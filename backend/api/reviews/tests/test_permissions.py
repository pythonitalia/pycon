import pytest

from conferences.tests.factories import ConferenceFactory
from reviews.models import ReviewSession, UserReview
from reviews.tests.factories import ReviewSessionFactory
from submissions.tests.factories import SubmissionFactory

pytestmark = pytest.mark.django_db

OPERATIONS = {
    "reviewSession": (
        "query($sessionId: ID!) { reviewSession(reviewSessionId: $sessionId) { id } }",
        lambda session_id, proposal_id, option_id: {"sessionId": session_id},
    ),
    "reviewProposal": (
        """query($sessionId: ID!, $proposalId: ID!) {
            reviewProposal(reviewSessionId: $sessionId, proposalId: $proposalId) { id }
        }""",
        lambda session_id, proposal_id, option_id: {
            "sessionId": session_id,
            "proposalId": proposal_id,
        },
    ),
    "nextProposalToReview": (
        """query($sessionId: ID!) {
            nextProposalToReview(reviewSessionId: $sessionId, excludeTags: [], seen: [])
        }""",
        lambda session_id, proposal_id, option_id: {"sessionId": session_id},
    ),
    "voteProposal": (
        """mutation($input: VoteProposalInput!) {
            voteProposal(input: $input) { __typename }
        }""",
        lambda session_id, proposal_id, option_id: {
            "input": {
                "reviewSessionId": session_id,
                "proposalId": proposal_id,
                "scoreOptionId": option_id,
                "comment": "",
            }
        },
    ),
}


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize(
    "caller",
    [
        "anonymous",
        "user",
        "staff_without_permissions",
        "reviewer_of_another_conference",
        "reviewer_of_a_grants_session",
    ],
)
def test_refuses_users_who_cannot_review(
    admin_graphql_api_client,
    user,
    admin_user,
    make_reviewer,
    proposals_review_session,
    operation,
    caller,
):
    review_session = proposals_review_session
    option = review_session.availablescoreoption_set.get()
    proposal = SubmissionFactory(conference=review_session.conference)

    if caller == "user":
        admin_graphql_api_client.force_login(user)
    elif caller == "staff_without_permissions":
        admin_graphql_api_client.force_login(admin_user)
    elif caller == "reviewer_of_another_conference":
        admin_graphql_api_client.force_login(make_reviewer(ConferenceFactory()))
    elif caller == "reviewer_of_a_grants_session":
        review_session = ReviewSessionFactory(
            conference=review_session.conference,
            session_type=ReviewSession.SessionType.GRANTS,
        )
        admin_graphql_api_client.force_login(make_reviewer(review_session.conference))

    query, build_variables = OPERATIONS[operation]
    response = admin_graphql_api_client.query(
        query, variables=build_variables(review_session.id, proposal.id, option.id)
    )

    assert response["errors"][0]["message"] == "Cannot review this session"
    assert not UserReview.objects.exists()
