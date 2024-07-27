from voting.tests.factories.ranking import RankRequestFactory, RankSubmissionFactory
from conferences.tests.factories import ConferenceFactory
import pytest

pytestmark = [pytest.mark.django_db]


def test_conference_ranking_does_not_exists(
    graphql_client,
):
    conference = ConferenceFactory(
        topics=[
            "Sushi",
        ]
    )

    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        rank
                        score
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
    conference_factory,
    rank_request_factory,
    graphql_client,
):
    conference = ConferenceFactory(
        topics=[
            "Sushi",
        ]
    )
    RankRequestFactory(conference=conference, is_public=False)
    query = """
        query($code: String!, $topic: ID!) {
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
    graphql_client,
):
    conference = ConferenceFactory()
    rank_request = RankRequestFactory(conference=conference, is_public=True)
    rank_submission = RankSubmissionFactory(rank_request=rank_request)
    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        rank
                        score
                    }
                }
            }
        }
    """

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "topic": str(rank_submission.submission.topic.id),
        },
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["ranking"]["isPublic"] is True

    rank_submission_data = resp["data"]["conference"]["ranking"]["rankedSubmissions"][0]

    assert rank_submission_data["rank"] == rank_submission.rank
    assert float(rank_submission_data["score"]) == float(rank_submission.score)


def test_conference_ranking_is_not_public_admin_can_see(
    graphql_client,
    admin_user,
):
    conference = ConferenceFactory()
    graphql_client.force_login(admin_user)
    rank_request = RankRequestFactory(conference=conference, is_public=False)
    rank_submission = RankSubmissionFactory(rank_request=rank_request)
    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        rank
                        score
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

    assert rank_submission_data["rank"] == rank_submission.rank
    assert float(rank_submission_data["score"]) == float(rank_submission.score)


def test_conference_ranking_is_not_public_users_cannot_see(
    graphql_client,
    user,
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)
    rank_request = RankRequestFactory(conference=conference, is_public=False)
    rank_submission = RankSubmissionFactory(
        rank_request=rank_request,
    )

    query = """
        query($code: String!, $topic: ID!) {
            conference(code: $code) {
                ranking(topic: $topic) {
                    isPublic
                    rankedSubmissions {
                        rank
                        score
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
