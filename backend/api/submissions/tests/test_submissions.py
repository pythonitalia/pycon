import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def mock_has_ticket(requests_mock, settings):
    def wrapper(conference):
        requests_mock.post(
            f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
            json={"user_has_admission_ticket": True},
        )

    return wrapper


@pytest.mark.skip
def test_returns_none_when_no_logged_in(graphql_client, submission_factory):
    submission = submission_factory()

    resp = graphql_client.query(
        """query Submissions($code: String!) {
            submissions(code: $code) {
                id
            }
        }""",
        variables={"code": submission.conference.code},
    )

    assert resp["errors"] == [
        {
            "locations": [{"column": 13, "line": 2}],
            "message": "Invalid or no token provided",
            "path": ["submissions"],
        }
    ]
    assert resp["data"]["submissions"] is None


@pytest.mark.skip
def test_returns_none_when_token_is_invalid(graphql_client, submission_factory):
    submission = submission_factory()

    resp = graphql_client.query(
        """query Submissions($code: String!) {
            submissions(code: $code) {
                id
            }
        }""",
        variables={"code": submission.conference.code},
        headers={"HTTP_AUTHORIZATION": "Token ABC"},
    )

    assert resp["errors"] == [
        {
            "locations": [{"column": 13, "line": 2}],
            "message": "Invalid or no token provided",
            "path": ["submissions"],
        }
    ]
    assert resp["data"]["submissions"] is None


@pytest.mark.skip
def test_returns_submission_with_valid_token(
    graphql_client, token_factory, submission_factory
):
    token = token_factory()
    submission = submission_factory()

    resp = graphql_client.query(
        """query Submissions($code: String!) {
            submissions(code: $code) {
                id
            }
        }""",
        variables={"code": submission.conference.code},
        headers={"X-Backend-Token": str(token)},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission.hashid}]


def test_returns_submissions_paginated(graphql_client, user, submission_factory):
    graphql_client.force_login(user)

    submission = submission_factory(id=1, speaker_id=user.id)
    submission_2 = submission_factory(id=2, conference=submission.conference)

    query = """query Submissions($code: String!, $after: String) {
        submissions(code: $code, after: $after, limit: 1) {
            id
        }
    }"""
    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission.hashid}]

    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "after": submission.hashid},
    )
    assert resp["data"]["submissions"] == [{"id": submission_2.hashid}]


def test_filter_submissions_by_language(
    graphql_client, user, submission_factory, mock_has_ticket
):
    graphql_client.force_login(user)
    submission = submission_factory(languages=["it", "en"])
    submission_factory(conference=submission.conference, languages=["it"])
    mock_has_ticket(submission.conference)

    query = """query Submissions($code: String!, $language: String!) {
        submissions(code: $code, language: $language) {
            id
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "language": "en"},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission.hashid}]


def test_filter_submissions_by_tags(
    graphql_client, user, submission_factory, mock_has_ticket
):
    graphql_client.force_login(user)
    submission = submission_factory(tags=["cat"])
    submission_factory(conference=submission.conference, tags=["dog", "bear"])
    submission_3 = submission_factory(
        conference=submission.conference, tags=["cat", "lion"]
    )
    mock_has_ticket(submission.conference)
    query = """query Submissions($code: String!, $tags: [String!]) {
        submissions(code: $code, tags: $tags) {
            id
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
    assert resp["data"]["submissions"] == [
        {"id": submission.hashid},
        {"id": submission_3.hashid},
    ]


def test_filter_by_user_voted_only(
    graphql_client, user, submission_factory, vote_factory, mock_has_ticket
):
    graphql_client.force_login(user)
    submission = submission_factory()
    submission_factory(conference=submission.conference)
    mock_has_ticket(submission.conference)
    vote_factory(user_id=user.id, submission=submission)

    query = """query Submissions($code: String!, $voted: Boolean!) {
        submissions(code: $code, voted: $voted) {
            id
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "voted": True},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission.hashid}]


def test_filter_by_user_has_not_voted(
    graphql_client, user, submission_factory, vote_factory, mock_has_ticket
):
    graphql_client.force_login(user)
    submission = submission_factory()
    submission_2 = submission_factory(conference=submission.conference)
    mock_has_ticket(submission.conference)
    vote_factory(user_id=user.id, submission=submission)

    query = """query Submissions($code: String!, $voted: Boolean!) {
        submissions(code: $code, voted: $voted) {
            id
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={"code": submission.conference.code, "voted": False},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission_2.hashid}]


def test_filter_by_type(
    graphql_client, user, conference_factory, submission_factory, mock_has_ticket
):
    graphql_client.force_login(user)
    conference = conference_factory(
        submission_types=("talk", "workshop"),
    )
    submission = submission_factory(
        conference=conference, custom_submission_type="talk"
    )
    submission_factory(conference=conference, custom_submission_type="workshop")
    mock_has_ticket(conference)

    query = """query Submissions($code: String!, $type: String!) {
        submissions(code: $code, type: $type) {
            id
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={"code": conference.code, "type": str(submission.type.id)},
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission.hashid}]


def test_filter_by_audience_level(
    graphql_client, user, conference_factory, submission_factory, mock_has_ticket
):
    graphql_client.force_login(user)
    conference = conference_factory(
        audience_levels=("adult", "senior"),
    )
    submission = submission_factory(
        conference=conference, custom_audience_level="adult"
    )
    submission_factory(conference=conference, custom_audience_level="senior")
    mock_has_ticket(conference)

    query = """query Submissions($code: String!, $audienceLevel: String!) {
        submissions(code: $code, audienceLevel: $audienceLevel) {
            id
        }
    }"""

    resp = graphql_client.query(
        query,
        variables={
            "code": conference.code,
            "audienceLevel": str(submission.audience_level.id),
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["submissions"] == [{"id": submission.hashid}]
