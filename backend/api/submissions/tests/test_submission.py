from pytest import mark

from api.helpers.ids import encode_hashid


@mark.django_db
def test_returns_none_when_missing(graphql_client):
    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": encode_hashid(11)},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"] is None


def test_can_only_see_title_if_not_logged(graphql_client, user, submission_factory):
    submission = submission_factory()

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
                title
                elevatorPitch
                previousTalkVideo
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"]["title"] == submission.title
    assert resp["data"]["submission"]["elevatorPitch"] is None
    assert resp["data"]["submission"]["previousTalkVideo"] is None


def test_can_see_submission_restricted_fields_if_has_ticket(
    graphql_client, user, submission_factory, mocker
):
    graphql_client.force_login(user)
    mocker.patch("voting.helpers.user_has_admission_ticket").return_value = True
    submission = submission_factory()

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
                elevatorPitch
                abstract
                topic {
                    name
                }
                type {
                    name
                }
                duration {
                    name
                }
                audienceLevel {
                    name
                }
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"]["elevatorPitch"] == submission.elevator_pitch
    assert resp["data"]["submission"]["abstract"] == submission.abstract
    assert resp["data"]["submission"]["topic"]["name"] == submission.topic.name
    assert resp["data"]["submission"]["type"]["name"] == submission.type.name
    assert resp["data"]["submission"]["duration"]["name"] == submission.duration.name
    assert (
        resp["data"]["submission"]["audienceLevel"]["name"]
        == submission.audience_level.name
    )


def test_can_see_submission_restricted_fields_if_has_sent_at_least_one_talk(
    graphql_client, user, submission_factory, mocker
):
    graphql_client.force_login(user)

    mocker.patch("voting.helpers.user_has_admission_ticket").return_value = False

    other_conference = submission_factory(speaker_id=user.id)
    submission = submission_factory(conference=other_conference.conference)

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
                elevatorPitch
                abstract
                topic {
                    name
                }
                type {
                    name
                }
                duration {
                    name
                }
                audienceLevel {
                    name
                }
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"]["elevatorPitch"] == submission.elevator_pitch
    assert resp["data"]["submission"]["abstract"] == submission.abstract
    assert resp["data"]["submission"]["topic"]["name"] == submission.topic.name
    assert resp["data"]["submission"]["type"]["name"] == submission.type.name
    assert resp["data"]["submission"]["duration"]["name"] == submission.duration.name
    assert (
        resp["data"]["submission"]["audienceLevel"]["name"]
        == submission.audience_level.name
    )


def test_can_see_all_submission_fields_if_speaker(
    graphql_client, user, submission_factory, mocker
):
    graphql_client.force_login(user)

    submission = submission_factory(
        speaker_id=user.id,
        languages=("it", "en"),
        tags=("python", "GraphQL"),
    )

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
                title
                slug
                elevatorPitch
                abstract
                speakerLevel
                previousTalkVideo
                topic {
                    name
                }
                type {
                    name
                }
                duration {
                    name
                }
                audienceLevel {
                    name
                }
                notes
                languages {
                    code
                }
                tags {
                    name
                }
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert resp["data"]["submission"]["title"] == submission.title
    assert resp["data"]["submission"]["slug"] == submission.slug
    assert resp["data"]["submission"]["elevatorPitch"] == submission.elevator_pitch
    assert resp["data"]["submission"]["abstract"] == submission.abstract
    assert resp["data"]["submission"]["speakerLevel"] == submission.speaker_level
    assert (
        resp["data"]["submission"]["previousTalkVideo"]
        == submission.previous_talk_video
    )
    assert resp["data"]["submission"]["topic"]["name"] == submission.topic.name
    assert resp["data"]["submission"]["type"]["name"] == submission.type.name
    assert resp["data"]["submission"]["duration"]["name"] == submission.duration.name
    assert (
        resp["data"]["submission"]["audienceLevel"]["name"]
        == submission.audience_level.name
    )
    assert resp["data"]["submission"]["notes"] == submission.notes
    assert resp["data"]["submission"]["languages"] == [{"code": "it"}, {"code": "en"}]
    assert resp["data"]["submission"]["tags"] == [
        {"name": "python"},
        {"name": "GraphQL"},
    ]


def test_can_see_all_restricted_submission_fields_if_vote_closed(
    graphql_client, user, submission_factory, conference_factory
):
    conference = conference_factory(active_voting=False)
    submission = submission_factory(conference=conference)

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
                title
                slug
                elevatorPitch
                abstract
                topic {
                    name
                }
                type {
                    name
                }
                duration {
                    name
                }
                audienceLevel {
                    name
                }
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert resp["data"]["submission"]["title"] == submission.title
    assert resp["data"]["submission"]["slug"] == submission.slug
    assert resp["data"]["submission"]["elevatorPitch"] == submission.elevator_pitch
    assert resp["data"]["submission"]["abstract"] == submission.abstract
    assert resp["data"]["submission"]["topic"]["name"] == submission.topic.name
    assert resp["data"]["submission"]["type"]["name"] == submission.type.name
    assert resp["data"]["submission"]["duration"]["name"] == submission.duration.name
    assert (
        resp["data"]["submission"]["audienceLevel"]["name"]
        == submission.audience_level.name
    )


@mark.django_db
def test_can_not_see_private_field(graphql_client, submission_factory):
    submission = submission_factory()

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
                speakerLevel
                previousTalkVideo
                notes
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert resp["data"]["submission"]["speakerLevel"] is None
    assert resp["data"]["submission"]["previousTalkVideo"] is None
    assert resp["data"]["submission"]["notes"] is None


def test_returns_correct_submission(graphql_client, user, submission_factory):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id)

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"]["id"] == submission.hashid


@mark.django_db
def test_user_can_edit_submission_if_within_cfp_time_and_is_the_owner(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id, conference__active_cfp=True)

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }
    """,
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"]["canEdit"] is True


@mark.django_db
def test_cannot_edit_submission_if_not_the_owner(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)
    submission = submission_factory(conference__active_cfp=True)

    response = graphql_client.query(
        """query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"] == {"id": submission.hashid, "canEdit": False}


@mark.django_db
def test_can_edit_submission_if_cfp_is_closed(graphql_client, user, submission_factory):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id, conference__active_cfp=False)

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }
    """,
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"]["canEdit"] is True


@mark.django_db
def test_get_submission_comments(graphql_client, user, submission_comment_factory):
    graphql_client.force_login(user)

    comment = submission_comment_factory()

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                comments {
                    id
                    text
                    author {
                        id
                    }
                }
            }
        }
    """,
        variables={"id": comment.submission.hashid},
    )

    assert len(response["data"]["submission"]["comments"]) == 1
    assert {
        "id": str(comment.id),
        "text": comment.text,
        "author": {"id": str(comment.author_id)},
    } in response["data"]["submission"]["comments"]


@mark.django_db
def test_get_submission_comments_returns_speaker_as_name(
    graphql_client, user, submission, submission_comment_factory
):
    graphql_client.force_login(user)

    comment = submission_comment_factory(
        submission=submission, author_id=submission.speaker_id
    )

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                comments {
                    id
                    text
                    author {
                        id
                    }
                }
            }
        }
    """,
        variables={"id": comment.submission.hashid},
    )

    assert len(response["data"]["submission"]["comments"]) == 1
    assert {
        "id": str(comment.id),
        "text": comment.text,
        "author": {"id": str(submission.speaker_id)},
    } == response["data"]["submission"]["comments"][0]
