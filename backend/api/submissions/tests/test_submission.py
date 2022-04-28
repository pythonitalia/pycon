from pytest import mark

from api.helpers.ids import encode_hashid


@mark.django_db
def test_returns_none_when_missing(graphql_client):
    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": encode_hashid(11)},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"] is None


def test_returns_correct_submission(graphql_client, user, submission_factory):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id)

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"]["id"] == submission.hashid


@mark.django_db
def test_user_can_edit_submission_if_within_cfp_time_and_is_the_owner(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id, conference__active_cfp=True)

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }
    """,
        variables={"id": submission.hashid},
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
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"] == {"id": submission.hashid, "canEdit": False}


@mark.django_db
def test_can_edit_submission_if_cfp_is_closed(graphql_client, user, submission_factory):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id, conference__active_cfp=False)

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }
    """,
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"]["canEdit"] is True


@mark.django_db
def test_get_submission_comments(
    graphql_client, user, submission_comment_factory, requests_mock, settings
):
    graphql_client.force_login(user)

    comment = submission_comment_factory()
    conference = comment.submission.conference

    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": True},
    )

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                comments {
                    id
                    text
                    author {
                        id
                    }
                }
            }
        }
    """,
        variables={"id": comment.submission.hashid},
    )

    assert len(response["data"]["submission"]["comments"]) == 1
    assert {
        "id": str(comment.id),
        "text": comment.text,
        "author": {"id": str(comment.author_id)},
    } in response["data"]["submission"]["comments"]


@mark.django_db
def test_get_submission_comments_returns_speaker_as_name(
    graphql_client,
    user,
    submission,
    submission_comment_factory,
    requests_mock,
    settings,
):
    conference = submission.conference
    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": True},
    )

    graphql_client.force_login(user)

    comment = submission_comment_factory(
        submission=submission, author_id=submission.speaker_id
    )

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                comments {
                    id
                    text
                    author {
                        id
                    }
                }
            }
        }
    """,
        variables={"id": comment.submission.hashid},
    )

    assert len(response["data"]["submission"]["comments"]) == 1
    assert {
        "id": str(comment.id),
        "text": comment.text,
        "author": {"id": str(submission.speaker_id)},
    } == response["data"]["submission"]["comments"][0]
