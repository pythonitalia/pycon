import strawberry

from api.context import Context
from api.reviews.permissions import CanReviewSession
from api.reviews.types import ReviewProposal, review_proposals_queryset
from reviews import models


@strawberry.field(permission_classes=[CanReviewSession])
def review_proposal(
    info: strawberry.Info[Context],
    review_session_id: strawberry.ID,
    proposal_id: strawberry.ID,
) -> ReviewProposal | None:
    review_session = models.ReviewSession.objects.get(id=review_session_id)
    proposal = review_proposals_queryset(review_session).filter(id=proposal_id).first()

    if not proposal:
        return None

    return ReviewProposal.from_model(
        proposal, review_session, info.context.request.user
    )
