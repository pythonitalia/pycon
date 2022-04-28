import respx
from pytest import mark

from submissions.models import SubmissionComment


def _send_comment(client, submission, text):
    return client.query(
        """
    mutation($input: SendSubmissionCommentInput!) {
        sendSubmissionComment(input: $input) {
            __typename

            ... on SubmissionComment {
                id
                text
                created
                author {
                    id
                }

                submission {
                    id
                }
            }

            ... on SendSubmissionCommentErrors {
                validationText: text
                validationSubmission: submission
                nonFieldErrors
            }
        }
    }
    """,
        variables={"input": {"submission": submission.hashid, "text": text}},
    )


@mark.django_db
def test_send_comment(
    graphql_client, user, submission, mocker, requests_mock, settings
):
    conference = submission.conference
    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket",
        json={"user_has_admission_ticket": True},
    )

    mocker.patch("notifications.aws.send_notification")

    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "Hello world!")

    assert resp["data"]["sendSubmissionComment"]["__typename"] == "SubmissionComment"
    assert resp["data"]["sendSubmissionComment"]["text"] == "Hello world!"
    assert resp["data"]["sendSubmissionComment"]["author"]["id"] == str(user.id)

    comment = SubmissionComment.objects.get(submission=submission, author_id=user.id)

    assert comment.text == "Hello world!"


@mark.django_db
def test_user_needs_a_ticket_to_comment(
    graphql_client, user, submission_factory, requests_mock, settings
):
    submission = submission_factory()
    conference = submission.conference
    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket",
        json={"user_has_admission_ticket": False},
    )

    graphql_client.force_login(user)

    with respx.mock as mock:
        mock.post(f"{settings.ASSOCIATION_BACKEND_SERVICE}/internal-api").respond(
            json={"data": {"userIdIsMember": False}}
        )
        resp = _send_comment(graphql_client, submission, "Hello world!")

    assert resp["errors"][0]["message"] == "You can't send a comment"


@mark.django_db
def test_cannot_send_comments_unauthenticated(
    graphql_client, submission_factory, mocker
):
    submission = submission_factory()

    resp = _send_comment(graphql_client, submission, "What are you doing here!")

    assert resp["errors"][0]["message"] == "User not logged in"


@mark.django_db
def test_staff_can_comment_submissions(
    graphql_client, admin_user, submission_factory, mocker
):
    mocker.patch("notifications.aws.send_notification")

    submission = submission_factory()

    graphql_client.force_login(admin_user)

    resp = _send_comment(graphql_client, submission, "What are you doing here!")

    assert not resp.get("errors")

    assert resp["data"]["sendSubmissionComment"]["__typename"] == "SubmissionComment"
    assert resp["data"]["sendSubmissionComment"]["submission"]


@mark.django_db
def test_speakers_can_comment_other_submissions(
    graphql_client, user, submission_factory, mocker
):
    mocker.patch("notifications.aws.send_notification")

    user_submission = submission_factory(speaker_id=user.id)
    submission = submission_factory(conference=user_submission.conference)

    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "Another submission!")

    assert resp["data"]["sendSubmissionComment"]["__typename"] == "SubmissionComment"


@mark.django_db
def test_user_can_send_comment_to_own_submission(
    graphql_client, user, submission_factory, mocker
):
    mocker.patch("notifications.aws.send_notification")
    submission = submission_factory(speaker_id=user.id)

    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "Hello world!")

    assert resp["data"]["sendSubmissionComment"]["__typename"] == "SubmissionComment"


def test_cannot_send_empty_comment(
    graphql_client, user, submission, requests_mock, settings
):
    conference = submission.conference
    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket",
        json={"user_has_admission_ticket": True},
    )

    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "")

    assert (
        resp["data"]["sendSubmissionComment"]["__typename"]
        == "SendSubmissionCommentErrors"
    )
    assert resp["data"]["sendSubmissionComment"]["validationText"] == [
        "This field is required."
    ]
