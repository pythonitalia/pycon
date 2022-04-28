from pytest import mark


@mark.django_db
def test_get_logged_user_vote_on_a_submission(
    graphql_client, user, vote_factory, settings, requests_mock
):
    vote = vote_factory(user_id=user.id, value=1)
    conference = vote.submission.conference

    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": True},
    )

    graphql_client.force_login(user)

    response = graphql_client.query(
        """query MyVote($conference: String!) {
        conference(code: $conference) {
            submissions {
                myVote {
                    value
                }
            }
        }
    }
    """,
        variables={"conference": conference.code},
    )

    assert response["data"]["conference"]["submissions"][0]["myVote"]["value"] == 1


@mark.django_db
def test_cannot_get_my_vote_as_unlogged(graphql_client, user, vote_factory):
    vote = vote_factory(user_id=user.id)

    response = graphql_client.query(
        """query MyVote($conference: String!) {
        conference(code: $conference) {
            submissions {
                myVote {
                    value
                }
            }
        }
    }
    """,
        variables={"conference": vote.submission.conference.code},
    )

    assert (
        response["errors"][0]["message"]
        == "You need to have a ticket to see submissions"
    )
    assert response["errors"][0]["path"] == ["conference", "submissions"]


@mark.django_db
def test_get_my_vote_when_the_user_never_voted(
    graphql_client, user, submission_factory, requests_mock, settings
):
    submission = submission_factory()
    conference = submission.conference

    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": True},
    )

    graphql_client.force_login(user)

    response = graphql_client.query(
        """query MyVote($conference: String!) {
        conference(code: $conference) {
            submissions {
                myVote {
                    value
                }
            }
        }
    }
    """,
        variables={"conference": conference.code},
    )

    assert response["data"]["conference"]["submissions"][0]["myVote"] is None
