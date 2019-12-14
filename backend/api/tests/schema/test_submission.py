from pytest import mark


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

    assert response["data"]["submission"] is None


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
