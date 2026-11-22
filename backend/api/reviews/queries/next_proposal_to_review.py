import strawberry

from api.context import Context
from api.reviews.permissions import CanReviewSession
from reviews import models
from reviews.adapters import ProposalsReviewAdapter


@strawberry.field(permission_classes=[CanReviewSession])
def next_proposal_to_review(
    info: strawberry.Info[Context],
    review_session_id: strawberry.ID,
    exclude_tags: list[strawberry.ID],
    seen: list[strawberry.ID],
) -> strawberry.ID | None:
    review_session = models.ReviewSession.objects.get(id=review_session_id)
    user = info.context.request.user
    adapter = ProposalsReviewAdapter()
    exclude = [int(tag_id) for tag_id in exclude_tags]
    seen_ids = [int(proposal_id) for proposal_id in seen]

    next_id = adapter.get_next_to_review_item_id(
        review_session, user, exclude=exclude, seen=seen_ids
    )

    if next_id is None and seen_ids:
        next_id = adapter.get_next_to_review_item_id(
            review_session, user, exclude=exclude, seen=seen_ids[-1:]
        )

    return strawberry.ID(str(next_id)) if next_id else None
