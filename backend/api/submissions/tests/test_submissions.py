from pytest import mark


@mark.django_db
@mark.skip
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
@mark.skip
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
@mark.skip
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
        headers={"X-Backend-Token": str(token)},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission.hashid}]


@mark.django_db
def test_returns_submissions_paginated(graphql_client, user, submission_factory):
    graphql_client.force_login(user)

    submission = submission_factory(id=1, speaker_id=user.id)
    submission_2 = submission_factory(id=2, conference=submission.conference)

    query = """query Submissions($code: String!, $after: String) {
        submissions(code: $code, after: $after, limit: 1) {
            id
        }
    }"""
    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission.hashid}]

    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "after": submission.hashid},
    )
    assert resp["data"]["submissions"] == [{"id": submission_2.hashid}]
