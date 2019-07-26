from pytest import mark


@mark.django_db
def test_get_logged_user_vote_on_a_submission(graphql_client, user, vote_factory):
    graphql_client.force_login(user)

    vote = vote_factory(user=user, value=0)

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
        response["data"]["conference"]["submissions"][0]["myVote"]["value"]
        == "NOT_INTERESTED"
    )


@mark.django_db
def test_cannot_get_my_vote_as_unlogged(graphql_client, user, vote_factory):
    vote = vote_factory(user=user)

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

    assert response["errors"][0]["message"] == "User not logged in"
    assert response["errors"][0]["path"] == ["conference", "submissions", 0, "myVote"]


@mark.django_db
def test_get_my_vote_when_the_user_never_voted(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)

    submission = submission_factory()

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
        variables={"conference": submission.conference.code},
    )

    assert response["data"]["conference"]["submissions"][0]["myVote"] is None
