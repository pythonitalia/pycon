import strawberry

from api.reviews.permissions import CanReviewSession
from api.reviews.types import ReviewSession
from reviews import models


@strawberry.field(permission_classes=[CanReviewSession])
def review_session(review_session_id: strawberry.ID) -> ReviewSession:
    return ReviewSession.from_model(
        models.ReviewSession.objects.get(id=review_session_id)
    )
