from pytest import mark


def _update_submission(
    graphql_client,
    *,
    submission,
    new_topic,
    new_audience,
    new_type,
    new_tag,
    new_duration,
    new_languages=["en"]
):
    return graphql_client.query(
        """
    mutation Submission($input: UpdateSubmissionInput!) {
        updateSubmission(input: $input) {
            __typename

            ... on Submission {
                id
                title
                notes
                abstract
                elevatorPitch

                topic {
                    name
                    id
                }

                audienceLevel {
                    id
                    name
                }

                languages {
                    code
                }

                type {
                    id
                    name
                }

                tags {
                    name
                    id
                }

                conference {
                    id
                    name
                }

                duration {
                    id
                    name
                }
            }

            ... on UpdateSubmissionErrors {
                nonFieldErrors: nonFieldErrors
                validationNotes: notes
                validationTopic: topic
                validationAbstract: abstract
                validationDuration: duration
                validationAudienceLevel: audienceLevel
                validationType: type
                validationLanguages: languages
            }
        }
    }
    """,
        variables={
            "input": {
                "instance": submission.id,
                "title": "new title to use",
                "elevatorPitch": "This is an elevator pitch",
                "abstract": "abstract here",
                "topic": new_topic.id,
                "audienceLevel": new_audience.id,
                "type": new_type.id,
                "languages": new_languages,
                "notes": "notes here",
                "tags": [new_tag.id],
                "duration": new_duration.id,
            }
        },
    )


@mark.django_db
def test_update_submission(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
        speaker=user,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
    )

    graphql_client.force_login(user)

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = submission_tag_factory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"

    assert {
        "__typename": "Submission",
        "id": str(submission.id),
        "title": "new title to use",
        "notes": "notes here",
        "abstract": "abstract here",
        "elevatorPitch": "This is an elevator pitch",
        "topic": {"name": new_topic.name, "id": str(new_topic.id)},
        "audienceLevel": {"id": str(new_audience.id), "name": new_audience.name},
        "languages": [{"code": "en"}],
        "type": {"id": str(new_type.id), "name": new_type.name},
        "tags": [{"name": new_tag.name, "id": str(new_tag.id)}],
        "conference": {
            "name": conference.name.localize("en"),
            "id": str(conference.id),
        },
        "duration": {"id": str(new_duration.id), "name": new_duration.name},
    } == response["data"]["updateSubmission"]


@mark.django_db
def test_cannot_update_submission_with_lang_outside_allowed_values(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en",),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
        speaker=user,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
    )

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = submission_tag_factory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_languages=["it"],
    )

    assert (
        response["data"]["updateSubmission"]["__typename"] == "UpdateSubmissionErrors"
    )

    assert response["data"]["updateSubmission"]["validationLanguages"] == [
        "Italian (it) is not an allowed language"
    ]


@mark.django_db
def test_cannot_edit_submission_outside_cfp(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en",),
        durations=("10", "20"),
        active_cfp=False,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
        speaker=user,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["en"],
        tags=["python", "ml"],
        conference=conference,
    )

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = submission_tag_factory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_languages=["it"],
    )

    assert (
        response["data"]["updateSubmission"]["__typename"] == "UpdateSubmissionErrors"
    )

    assert response["data"]["updateSubmission"]["nonFieldErrors"] == [
        "The call for papers is not open!"
    ]


@mark.django_db
def test_cannot_edit_submission_if_not_the_owner(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en",),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["en"],
        tags=["python", "ml"],
        conference=conference,
    )

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = submission_tag_factory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_languages=["en"],
    )

    assert (
        response["data"]["updateSubmission"]["__typename"] == "UpdateSubmissionErrors"
    )

    assert response["data"]["updateSubmission"]["nonFieldErrors"] == [
        "You cannot edit this submission"
    ]
