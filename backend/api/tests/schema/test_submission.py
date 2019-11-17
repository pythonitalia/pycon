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
