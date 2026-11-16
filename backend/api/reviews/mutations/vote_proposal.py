from typing import Annotated

import strawberry

from api.context import Context
from api.reviews.permissions import CanReviewSession
from api.reviews.types import ReviewProposal, review_proposals_queryset
from api.types import NotFound
from reviews import models


@strawberry.input
class VoteProposalInput:
    review_session_id: strawberry.ID
    proposal_id: strawberry.ID
    score_option_id: strawberry.ID | None
    comment: str


VoteProposalResult = Annotated[
    ReviewProposal | NotFound,
    strawberry.union(name="VoteProposalResult"),
]


@strawberry.field(permission_classes=[CanReviewSession])
def vote_proposal(
    info: strawberry.Info[Context], input: VoteProposalInput
) -> VoteProposalResult:
    review_session = models.ReviewSession.objects.get(id=input.review_session_id)
    user = info.context.request.user
    proposal = (
        review_proposals_queryset(review_session).filter(id=input.proposal_id).first()
    )
    score_option = (
        review_session.availablescoreoption_set.filter(id=input.score_option_id).first()
        if input.score_option_id
        else None
    )

    if not proposal or (input.score_option_id and not score_option):
        return NotFound()

    models.UserReview.objects.update_or_create(
        user=user,
        review_session=review_session,
        proposal=proposal,
        defaults={"score": score_option, "comment": input.comment},
    )

    return ReviewProposal.from_model(proposal, review_session, user)
