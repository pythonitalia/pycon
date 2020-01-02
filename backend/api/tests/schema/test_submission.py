from pytest import mark


@mark.django_db
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


@mark.parametrize("logged_in", (True, False))
def test_can_only_see_title_if_not_submitter_or_not_logged_in(
    logged_in, graphql_client, user, submission_factory
):
    submission = submission_factory()

    if logged_in:
        graphql_client.force_login(user)
        assert submission.speaker != user

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
                title
                elevatorPitch
            }
        }""",
        variables={"id": submission.id},
    )

    assert resp["errors"][0] == {
        "message": "You can't see details for this submission",
        "locations": [{"line": 5, "column": 17}],
        "path": ["submission", "elevatorPitch"],
    }

    assert resp["data"]["submission"]["title"] == submission.title
    assert resp["data"]["submission"]["elevatorPitch"] is None


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


@mark.django_db
def test_user_can_edit_submission_if_within_cfp_time_and_is_the_owner(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)
    submission = submission_factory(speaker=user, conference__active_cfp=True)

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }
    """,
        variables={"id": submission.id},
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
        variables={"id": submission.id},
    )

    assert response["data"]["submission"] == {
        "id": str(submission.id),
        "canEdit": False,
    }


@mark.django_db
def test_cannot_edit_submission_if_cfp_is_closed(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)
    submission = submission_factory(speaker=user, conference__active_cfp=False)

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }
    """,
        variables={"id": submission.id},
    )

    assert response["data"]["submission"]["canEdit"] is False
