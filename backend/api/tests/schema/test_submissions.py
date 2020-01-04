from pytest import mark


@mark.django_db
def test_returns_none_when_no_logged_in(graphql_client, submission_factory):
    submission = submission_factory()

    resp = graphql_client.query(
        """query Submissions($code: String!) {
            submissions(code: $code) {
                id
            }
        }""",
        variables={"code": submission.conference.code},
    )

    assert resp["errors"] == [
        {
            "locations": [{"column": 13, "line": 2}],
            "message": "Invalid or no token provided",
            "path": ["submissions"],
        }
    ]
    assert resp["data"]["submissions"] is None


@mark.django_db
def test_returns_none_when_token_is_invalid(graphql_client, submission_factory):
    submission = submission_factory()

    resp = graphql_client.query(
        """query Submissions($code: String!) {
            submissions(code: $code) {
                id
            }
        }""",
        variables={"code": submission.conference.code},
        headers={"HTTP_AUTHORIZATION": "Token ABC"},
    )

    assert resp["errors"] == [
        {
            "locations": [{"column": 13, "line": 2}],
            "message": "Invalid or no token provided",
            "path": ["submissions"],
        }
    ]
    assert resp["data"]["submissions"] is None


@mark.django_db
def test_returns_submission_with_valid_token(
    graphql_client, token_factory, submission_factory
):
    token = token_factory()
    submission = submission_factory()

    resp = graphql_client.query(
        """query Submissions($code: String!) {
            submissions(code: $code) {
                id
            }
        }""",
        variables={"code": submission.conference.code},
        headers={"HTTP_AUTHORIZATION": f"Token {token}"},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": str(submission.id)}]
