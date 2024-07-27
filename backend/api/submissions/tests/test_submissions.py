from voting.tests.factories.vote import VoteFactory
from conferences.tests.factories import ConferenceFactory
from submissions.tests.factories import SubmissionFactory
import pytest

pytestmark = pytest.mark.django_db


def test_returns_submissions_paginated(graphql_client, user):
    graphql_client.force_login(user)

    submission = SubmissionFactory(id=1, speaker_id=user.id)
    submission_2 = SubmissionFactory(id=2, conference=submission.conference)

    query = """query Submissions($code: String!, $page: Int) {
        submissions(code: $code, page: $page, pageSize: 1) {
            pageInfo {
                totalPages
                totalItems
            }
            items {
                id
            }
        }
    }"""
    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"]["items"] == [{"id": submission.hashid}]
    assert resp["data"]["submissions"]["pageInfo"] == {"totalPages": 2, "totalItems": 2}

    resp_2 = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "page": 2},
    )
    assert resp_2["data"]["submissions"]["items"] == [{"id": submission_2.hashid}]


def test_page_size_cannot_be_less_than_1(graphql_client, user):
    graphql_client.force_login(user)

    submission = SubmissionFactory(id=1, speaker_id=user.id)

    query = """query Submissions($code: String!) {
        submissions(code: $code, pageSize: -1) {
            pageInfo {
                totalPages
                totalItems
            }
            items {
                id
            }
        }
    }"""
    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code},
    )

    assert resp["errors"][0]["message"] == "Page size must be greater than 0"
    assert resp["data"]["submissions"] is None


def test_max_allowed_page_size(graphql_client, user):
    graphql_client.force_login(user)

    submission = SubmissionFactory(id=1, speaker_id=user.id)

    query = """query Submissions($code: String!) {
        submissions(code: $code, pageSize: 3000) {
            pageInfo {
                totalPages
                totalItems
            }
            items {
                id
            }
        }
    }"""
    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code},
    )

    assert resp["errors"][0]["message"] == "Page size cannot be greater than 150"
    assert resp["data"]["submissions"] is None


def test_min_allowed_page(graphql_client, user):
    graphql_client.force_login(user)

    submission = SubmissionFactory(id=1, speaker_id=user.id)

    query = """query Submissions($code: String!, $page: Int) {
        submissions(code: $code, page: $page) {
            pageInfo {
                totalPages
                totalItems
            }
            items {
                id
            }
        }
    }"""
    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "page": -1},
    )

    assert resp["errors"][0]["message"] == "Page must be greater than 0"
    assert resp["data"]["submissions"] is None


def test_filter_submissions_by_language(graphql_client, user, mock_has_ticket):
    graphql_client.force_login(user)
    submission = SubmissionFactory(languages=["it", "en"])
    SubmissionFactory(conference=submission.conference, languages=["it"])
    mock_has_ticket(submission.conference)

    query = """query Submissions($code: String!, $languages: [String!]) {
        submissions(code: $code, languages: $languages) {
            items {
                id
            }
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "languages": ["en"]},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"]["items"] == [{"id": submission.hashid}]


def test_filter_submissions_by_tags(graphql_client, user, mock_has_ticket):
    graphql_client.force_login(user)
    submission = SubmissionFactory(tags=["cat"])
    SubmissionFactory(conference=submission.conference, tags=["dog", "bear"])
    submission_3 = SubmissionFactory(
        conference=submission.conference, tags=["cat", "lion"]
    )
    mock_has_ticket(submission.conference)
    query = """query Submissions($code: String!, $tags: [String!]) {
        submissions(code: $code, tags: $tags) {
            items {
                id
            }
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={
            "code": submission.conference.code,
            "tags": [str(submission.tags.first().id), str(submission_3.tags.last().id)],
        },
    )

    assert not resp.get("errors")
    assert {"id": submission.hashid} in resp["data"]["submissions"]["items"]
    assert {"id": submission_3.hashid} in resp["data"]["submissions"]["items"]


def test_filter_by_user_voted_only(graphql_client, user, mock_has_ticket):
    graphql_client.force_login(user)
    submission = SubmissionFactory()
    SubmissionFactory(conference=submission.conference)
    mock_has_ticket(submission.conference)
    VoteFactory(user_id=user.id, submission=submission)

    query = """query Submissions($code: String!, $voted: Boolean!) {
        submissions(code: $code, voted: $voted) {
            items {
                id
            }
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "voted": True},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"]["items"] == [{"id": submission.hashid}]


def test_filter_by_user_has_not_voted(graphql_client, user, mock_has_ticket):
    graphql_client.force_login(user)
    submission = SubmissionFactory()
    submission_2 = SubmissionFactory(conference=submission.conference)
    mock_has_ticket(submission.conference)
    VoteFactory(user_id=user.id, submission=submission)

    query = """query Submissions($code: String!, $voted: Boolean!) {
        submissions(code: $code, voted: $voted) {
            items {
                id
            }
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "voted": False},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"]["items"] == [{"id": submission_2.hashid}]


def test_filter_by_type(graphql_client, user, mock_has_ticket):
    graphql_client.force_login(user)
    conference = ConferenceFactory(
        submission_types=("talk", "workshop"),
    )
    submission = SubmissionFactory(conference=conference, custom_submission_type="talk")
    SubmissionFactory(conference=conference, custom_submission_type="workshop")
    mock_has_ticket(conference)

    query = """query Submissions($code: String!, $types: [String!]) {
        submissions(code: $code, types: $types) {
            items {
                id
            }
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={"code": conference.code, "types": [str(submission.type.id)]},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"]["items"] == [{"id": submission.hashid}]


def test_filter_by_audience_level(graphql_client, user, mock_has_ticket):
    graphql_client.force_login(user)
    conference = ConferenceFactory(
        audience_levels=("adult", "senior"),
    )
    submission = SubmissionFactory(conference=conference, custom_audience_level="adult")
    SubmissionFactory(conference=conference, custom_audience_level="senior")
    mock_has_ticket(conference)

    query = """query Submissions($code: String!, $audienceLevels: [String!]) {
        submissions(code: $code, audienceLevels: $audienceLevels) {
            items {
                id
            }
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "audienceLevels": [str(submission.audience_level.id)],
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"]["items"] == [{"id": submission.hashid}]
