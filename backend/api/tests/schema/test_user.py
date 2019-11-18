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
    assert response["data"]["me"]["submissions"][0]["id"] == submission.hashid


def test_register_to_newsletter(graphql_client):
    email = "john@doe.com"

    query = """
        mutation($email: String!) {
            registerToNewsletter(input: {email: $email}) {
                __typename
                ... on RegisterToNewsletterErrors {
                    email
                    nonFieldErrors
                }
            }
        }
    """
    resp = graphql_client.query(query, variables={"email": email})
    print(resp)
    assert resp
