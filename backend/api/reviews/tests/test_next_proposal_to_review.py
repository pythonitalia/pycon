import pytest

from reviews.tests.factories import UserReviewFactory
from submissions.tests.factories import SubmissionFactory

pytestmark = pytest.mark.django_db

QUERY = """query($sessionId: ID!, $seen: [ID!]!) {
    nextProposalToReview(reviewSessionId: $sessionId, excludeTags: [], seen: $seen)
}"""


def _next(client, review_session, seen):
    return client.query(
        QUERY,
        variables={"sessionId": review_session.id, "seen": [str(id) for id in seen]},
    )["data"]["nextProposalToReview"]


def test_skipped_proposals_come_back_once_nothing_new_is_left(
    admin_graphql_api_client, make_reviewer, proposals_review_session
):
    review_session = proposals_review_session
    reviewer = make_reviewer(review_session.conference)
    first = SubmissionFactory(conference=review_session.conference)
    second = SubmissionFactory(conference=review_session.conference)
    admin_graphql_api_client.force_login(reviewer)

    assert _next(admin_graphql_api_client, review_session, [first.id]) == str(second.id)
    assert _next(
        admin_graphql_api_client, review_session, [first.id, second.id]
    ) == str(first.id)


def test_nothing_left_when_everything_is_voted(
    admin_graphql_api_client, make_reviewer, proposals_review_session
):
    review_session = proposals_review_session
    reviewer = make_reviewer(review_session.conference)
    proposal = SubmissionFactory(conference=review_session.conference)
    UserReviewFactory(
        review_session=review_session,
        proposal=proposal,
        user=reviewer,
        score=review_session.availablescoreoption_set.get(),
    )
    admin_graphql_api_client.force_login(reviewer)

    assert _next(admin_graphql_api_client, review_session, [proposal.id]) is None
