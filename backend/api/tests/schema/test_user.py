import pytest


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
def test_query_user_tickets(graphql_client, user, ticket_factory):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)

    response = graphql_client.query(
        """
    query ($conference: String!) {
        me {
            tickets(conference: $conference) {
                id
            }
        }
    }
    """,
        variables={"conference": ticket.ticket_fare.conference.code},
    )

    assert "errors" not in response
    assert len(response["data"]["me"]["tickets"]) == 1
    assert response["data"]["me"]["tickets"][0]["id"] == str(ticket.id)


@pytest.mark.django_db
def test_query_submissions(graphql_client, user, submission_factory):
    graphql_client.force_login(user)

    submission = submission_factory(speaker=user)

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
    assert response["data"]["me"]["submissions"][0]["id"] == str(submission.id)
