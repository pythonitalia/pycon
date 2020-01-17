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
                    name
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
def test_send_comment(graphql_client, user, submission, mocker):
    mocker.patch("notifications.aws.send_comment_notification")

    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "Hello world!")

    assert resp["data"]["sendSubmissionComment"]["__typename"] == "SubmissionComment"
    assert resp["data"]["sendSubmissionComment"]["text"] == "Hello world!"
    assert resp["data"]["sendSubmissionComment"]["author"]["name"] == "Speaker"

    comment = SubmissionComment.objects.get(submission=submission, author=user)

    assert comment.text == "Hello world!"


@mark.django_db
def test_user_needs_a_ticket_to_comment(
    graphql_client, user, submission_factory, mocker
):
    submission = submission_factory()
    mocker.patch("users.models.user_has_admission_ticket").return_value = False

    graphql_client.force_login(user)

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
    graphql_client, user, submission_factory, mocker
):
    mocker.patch("notifications.aws.send_comment_notification")

    user.is_staff = True
    user.save()
    submission = submission_factory()

    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "What are you doing here!")

    assert resp["data"]["sendSubmissionComment"]["__typename"] == "SubmissionComment"


@mark.django_db
def test_speakers_can_comment_other_submissions(
    graphql_client, user, submission_factory, mocker
):
    mocker.patch("notifications.aws.send_comment_notification")

    user_submission = submission_factory(speaker=user)
    submission = submission_factory(conference=user_submission.conference)

    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "Another submission!")

    assert resp["data"]["sendSubmissionComment"]["__typename"] == "SubmissionComment"


@mark.django_db
def test_user_can_send_comment_to_own_submission(
    graphql_client, user, submission_factory, mocker
):
    mocker.patch("notifications.aws.send_comment_notification")
    submission = submission_factory(speaker=user)

    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "Hello world!")

    assert resp["data"]["sendSubmissionComment"]["__typename"] == "SubmissionComment"


def test_cannot_send_empty_comment(graphql_client, user, submission):
    graphql_client.force_login(user)

    resp = _send_comment(graphql_client, submission, "")

    assert (
        resp["data"]["sendSubmissionComment"]["__typename"]
        == "SendSubmissionCommentErrors"
    )
    assert resp["data"]["sendSubmissionComment"]["validationText"] == [
        "This field is required."
    ]
