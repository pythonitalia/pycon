from pytest import mark

pytestmark = mark.django_db


def test_conference_ranking_does_not_exists(conference_factory, graphql_client):
    conference = conference_factory()
    query = """
        query($code: String!, $topic: String!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        absoluteRank
                        topicRank
                        absoluteScore
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={"code": conference.code, "topic": conference.topics.first().id},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"] is None


def test_conference_ranking_is_not_public(
    conference, rank_request_factory, graphql_client
):
    rank_request_factory(conference=conference, is_public=False)
    query = """
        query($code: String!, $topic: String!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={"code": conference.code, "topic": conference.topics.first().id},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"] is None


def test_conference_ranking_is_public_anyone_can_see(
    conference, rank_request_factory, rank_submission_factory, graphql_client
):
    rank_request = rank_request_factory(conference=conference, is_public=True)
    rank_submission = rank_submission_factory(rank_request=rank_request)
    query = """
        query($code: String!, $topic: String!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        absoluteRank
                        topicRank
                        absoluteScore
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "topic": rank_submission.submission.topic.id,
        },
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"]["isPublic"] is True

    rank_submission_data = resp["data"]["conference"]["ranking"]["rankedSubmissions"][0]

    assert rank_submission_data["absoluteRank"] == rank_submission.absolute_rank
    assert rank_submission_data["topicRank"] == rank_submission.topic_rank
    assert float(rank_submission_data["absoluteScore"]) == float(
        rank_submission.absolute_score
    )


def test_conference_ranking_is_not_public_admin_can_see(
    conference,
    rank_request_factory,
    rank_submission_factory,
    graphql_client,
    admin_user,
):
    graphql_client.force_login(admin_user)
    rank_request = rank_request_factory(conference=conference, is_public=False)
    rank_submission = rank_submission_factory(rank_request=rank_request)
    query = """
        query($code: String!, $topic: String!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        absoluteRank
                        topicRank
                        absoluteScore
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "topic": rank_submission.submission.topic.id,
        },
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"]["isPublic"] is False

    rank_submission_data = resp["data"]["conference"]["ranking"]["rankedSubmissions"][0]

    assert rank_submission_data["absoluteRank"] == rank_submission.absolute_rank
    assert rank_submission_data["topicRank"] == rank_submission.topic_rank
    assert float(rank_submission_data["absoluteScore"]) == float(
        rank_submission.absolute_score
    )


def test_conference_ranking_is_not_public_users_cannot_see(
    conference,
    rank_request_factory,
    rank_submission_factory,
    graphql_client,
    user,
):
    graphql_client.force_login(user)
    rank_request = rank_request_factory(conference=conference, is_public=False)
    rank_submission = rank_submission_factory(rank_request=rank_request)
    query = """
        query($code: String!, $topic: String!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        absoluteRank
                        topicRank
                        absoluteScore
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "topic": rank_submission.submission.topic.id,
        },
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"] is None
