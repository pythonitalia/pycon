from api.permissions import IsStaffPermission
from reviews import models


class CanReviewSession(IsStaffPermission):
    message = "Cannot review this session"

    def has_permission(self, source, info, **kwargs):
        if not super().has_permission(source, info, **kwargs):
            return False

        if input := kwargs.get("input"):
            review_session_id = input.review_session_id
        else:
            review_session_id = kwargs.get("review_session_id")

        review_session = models.ReviewSession.objects.filter(
            id=review_session_id
        ).first()

        if not review_session or not review_session.is_proposals_review:
            return False

        return review_session.user_can_review(info.context.request.user)
