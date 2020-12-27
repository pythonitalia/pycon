from pytest import mark


@mark.django_db
def test_get_conference_ranking_empty(conference_factory, graphql_client):
    conference = conference_factory()

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                ranking {
                    absoluteRank
                    topicRank
                    absoluteScore
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"] == []


@mark.django_db
def test_get_ranking(
    conference, rank_request_factory, rank_submission_factory, graphql_client
):
    rank_request = rank_request_factory(conference=conference)
    rank_submission = rank_submission_factory(rank_request=rank_request)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                ranking {
                    absoluteRank
                    topicRank
                    absoluteScore
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert len(resp["data"]["conference"]["ranking"])

    rank_submission_data = resp["data"]["conference"]["ranking"][0]

    assert rank_submission_data["absoluteRank"] == rank_submission.absolute_rank
    assert rank_submission_data["topicRank"] == rank_submission.topic_rank
    assert float(rank_submission_data["absoluteScore"]) == float(
        rank_submission.absolute_score
    )
