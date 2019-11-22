import pytest


def test_returns_none_when_missing(graphql_client):
    resp = graphql_client.query(
        """{
            submission(id: 1) {
                id
            }
        }"""
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"] is None


def test_returns_none_if_speaker_is_not_current(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)
    submission = submission_factory()

    assert submission.speaker != user

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": submission.id},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"] is None


def test_returns_correct_submission(graphql_client, user, submission_factory):
    graphql_client.force_login(user)
    submission = submission_factory(speaker=user)

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": submission.id},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"]["id"] == str(submission.id)


@pytest.mark.django_db
def test_submission_tag_get_or_create(graphql_client, user, submission_tag_factory):
    graphql_client.force_login(user)

    query = """
        mutation($name: String!) {
            sendTag(input: {
                name: $name
            }) {
                __typename
                ... on SubmissionTag{
                    name
                }
                ... on SendTagErrors {
                    nonFieldErrors
                }
            }
        }
    """
    resp = graphql_client.query(query, variables={"name": "Python"})

    assert resp["data"]["sendTag"]["__typename"] == "SubmissionTag"
    assert resp["data"]["sendTag"]["name"] == "Python"
