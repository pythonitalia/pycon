from pytest import mark

from submissions.models import Submission

pytestmark = mark.django_db


def _update_submission(
    graphql_client,
    *,
    submission,
    new_topic,
    new_audience,
    new_type,
    new_tag,
    new_duration,
    new_title=None,
    new_elevator_pitch=None,
    new_abstract=None,
    new_previous_talk_video="",
    new_speaker_level=Submission.SPEAKER_LEVELS.new,
    new_languages=["en"],
    new_short_social_summary=""
):
    new_title = new_title or {"en": "new title to use"}
    new_elevator_pitch = new_elevator_pitch or {"en": "This is an elevator pitch"}
    new_abstract = new_abstract or {"en": "abstract here"}
    short_social_summary = new_short_social_summary or ""

    return graphql_client.query(
        """
    mutation Submission($input: UpdateSubmissionInput!) {
        updateSubmission(input: $input) {
            __typename

            ... on Submission {
                id
                title(language: "en")
                notes
                abstract(language: "en")
                elevatorPitch(language: "en")
                shortSocialSummary

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

                speakerLevel
                previousTalkVideo
            }

            ... on SendSubmissionErrors {
                nonFieldErrors
                validationTitle: title
                validationNotes: notes
                validationTopic: topic
                validationAbstract: abstract
                validationDuration: duration
                validationAudienceLevel: audienceLevel
                validationType: type
                validationLanguages: languages
                validationPreviousTalkVideo: previousTalkVideo
                validationPreviousSpeakerLevel: speakerLevel
            }
        }
    }
    """,
        variables={
            "input": {
                "instance": submission.hashid,
                "title": new_title,
                "elevatorPitch": new_elevator_pitch,
                "abstract": new_abstract,
                "topic": new_topic.id,
                "audienceLevel": new_audience.id,
                "type": new_type.id,
                "languages": new_languages,
                "notes": "notes here",
                "tags": [new_tag.id],
                "duration": new_duration.id,
                "speakerLevel": new_speaker_level,
                "previousTalkVideo": new_previous_talk_video,
                "shortSocialSummary": short_social_summary,
            }
        },
    )


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
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
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
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_short_social_summary="test",
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"

    assert {
        "__typename": "Submission",
        "id": submission.hashid,
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
        "speakerLevel": "experienced",
        "previousTalkVideo": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "shortSocialSummary": "test",
    } == response["data"]["updateSubmission"]


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
        speaker_id=user.id,
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

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"

    assert response["data"]["updateSubmission"]["validationLanguages"] == [
        "Language (it) is not allowed"
    ]


def test_can_edit_submission_outside_cfp(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=False,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
        speaker_id=user.id,
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

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"
    submission = Submission.objects.get(id=submission.id)
    assert list(submission.languages.values_list("code", flat=True)) == ["en"]


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

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"

    assert response["data"]["updateSubmission"]["nonFieldErrors"] == [
        "You cannot edit this submission"
    ]


def test_make_submission_multi_lingual(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["en"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
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
        new_title={
            "en": "English",
            "it": "Italian",
        },
        new_elevator_pitch={
            "en": "Elevator English",
            "it": "Elevator Italian",
        },
        new_abstract={
            "en": "Abstract English",
            "it": "Abstract Italian",
        },
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_languages=["en", "it"],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"

    submission.refresh_from_db()

    assert submission.title.localize("en") == "English"
    assert submission.title.localize("it") == "Italian"

    assert submission.elevator_pitch.localize("en") == "Elevator English"
    assert submission.elevator_pitch.localize("it") == "Elevator Italian"

    assert submission.abstract.localize("en") == "Abstract English"
    assert submission.abstract.localize("it") == "Abstract Italian"


def test_edit_submission_multi_lingual_fields_required(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["en"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
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
        new_title={
            "en": "English",
            "it": "",
        },
        new_elevator_pitch={
            "en": "Elevator English",
            "it": "",
        },
        new_abstract={
            "en": "Abstract English",
            "it": "",
        },
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_languages=["en", "it"],
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["validationAbstract"] == [
        "Italian: Cannot be empty"
    ]
    assert response["data"]["updateSubmission"]["validationTitle"] == [
        "Italian: Cannot be empty"
    ]

    assert submission.languages.count() == 1
