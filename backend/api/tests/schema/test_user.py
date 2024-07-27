from submissions.tests.factories import SubmissionFactory
import pytest

pytestmark = pytest.mark.skip


def test_fails_when_user_is_not_authenticated(graphql_client):
    resp = graphql_client.query(
        """
        {
            me {
                email
            }
        }
        """
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


def test_works_when_user_is_logged_in(user, graphql_client):
    graphql_client.force_login(user)

    resp = graphql_client.query(
        """
        {
            me {
                email
            }
        }
        """
    )

    assert "errors" not in resp
    assert resp["data"]["me"]["email"] == user.email


@pytest.mark.django_db
def test_query_submissions(graphql_client, user):
    graphql_client.force_login(user)

    submission = SubmissionFactory(speaker_id=user.id)

    response = graphql_client.query(
        """query Submissions($conference: String!) {
            me {
                submissions(conference: $conference) {
                    id
                }
            }
        }""",
        variables={"conference": submission.conference.code},
    )

    assert "errors" not in response
    assert len(response["data"]["me"]["submissions"]) == 1
    assert response["data"]["me"]["submissions"][0]["id"] == submission.hashid


def test_can_edit_schedule(user, graphql_client):
    graphql_client.force_login(user)

    resp = graphql_client.query(
        """
        {
            me {
                canEditSchedule
            }
        }
        """
    )

    assert "errors" not in resp
    assert resp["data"]["me"]["canEditSchedule"] is False
