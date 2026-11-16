import pytest

from reviews.models import UserReview
from reviews.tests.factories import AvailableScoreOptionFactory, UserReviewFactory
from submissions.tests.factories import SubmissionFactory

pytestmark = pytest.mark.django_db

MUTATION = """mutation($input: VoteProposalInput!) {
    voteProposal(input: $input) {
        __typename
        ... on ReviewProposal { myVote { scoreOptionId comment } }
    }
}"""


def _vote(client, review_session, proposal, option, comment=""):
    return client.query(
        MUTATION,
        variables={
            "input": {
                "reviewSessionId": review_session.id,
                "proposalId": proposal.id,
                "scoreOptionId": option.id,
                "comment": comment,
            }
        },
    )["data"]["voteProposal"]


def test_vote_proposal_updates_the_same_vote_keeping_private_comment(
    admin_graphql_api_client, make_reviewer, proposals_review_session
):
    review_session = proposals_review_session
    reviewer = make_reviewer(review_session.conference)
    proposal = SubmissionFactory(conference=review_session.conference)
    no = review_session.availablescoreoption_set.get()
    yes = AvailableScoreOptionFactory(review_session=review_session, numeric_value=2)
    UserReviewFactory(
        review_session=review_session,
        proposal=proposal,
        user=reviewer,
        score=no,
        comment="Old",
        private_comment="Secret",
    )
    admin_graphql_api_client.force_login(reviewer)

    result = _vote(admin_graphql_api_client, review_session, proposal, yes, "New")

    assert result["myVote"] == {"scoreOptionId": str(yes.id), "comment": "New"}
    vote = UserReview.objects.get()
    assert vote.score == yes
    assert vote.comment == "New"
    assert vote.private_comment == "Secret"


@pytest.mark.parametrize("case", ["option_of_another_session", "cancelled_proposal"])
def test_vote_proposal_not_found(
    admin_graphql_api_client, make_reviewer, proposals_review_session, case
):
    review_session = proposals_review_session
    option = review_session.availablescoreoption_set.get()
    proposal = SubmissionFactory(conference=review_session.conference)
    if case == "option_of_another_session":
        option = AvailableScoreOptionFactory()
    else:
        proposal = SubmissionFactory(
            conference=review_session.conference, status="cancelled"
        )
    admin_graphql_api_client.force_login(make_reviewer(review_session.conference))

    result = _vote(admin_graphql_api_client, review_session, proposal, option)

    assert result["__typename"] == "NotFound"
    assert not UserReview.objects.exists()


def test_vote_proposal_no_vote_clears_the_score(
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

    result = admin_graphql_api_client.query(
        MUTATION,
        variables={
            "input": {
                "reviewSessionId": review_session.id,
                "proposalId": proposal.id,
                "scoreOptionId": None,
                "comment": "My own talk",
            }
        },
    )["data"]["voteProposal"]

    assert result["myVote"] == {"scoreOptionId": None, "comment": "My own talk"}
    assert UserReview.objects.get().score is None
