from typing import List, TYPE_CHECKING

from reviews.interfaces import ReviewWorkflow

if TYPE_CHECKING:
    from reviews.models import ReviewSession


class StandardReviewWorkflow(ReviewWorkflow):
    """Standard review workflow for most review sessions."""

    def can_start_review(self, review_session: "ReviewSession") -> bool:
        """Check if a review session can be started."""
        return review_session.status == review_session.Status.REVIEWING

    def can_see_recap(self, review_session: "ReviewSession") -> bool:
        """Check if recap can be viewed for this session."""
        if review_session.is_proposals_review:
            return True

        if review_session.is_grants_review and review_session.is_completed:
            return True

        return False

    def get_allowed_status_transitions(
        self, current_status: str, has_reviews: bool
    ) -> List[str]:
        """Return allowed status transitions based on current state."""
        from reviews.models import ReviewSession

        if current_status == ReviewSession.Status.DRAFT:
            return [ReviewSession.Status.REVIEWING]

        elif current_status == ReviewSession.Status.REVIEWING:
            if has_reviews:
                return [ReviewSession.Status.COMPLETED]
            else:
                return [ReviewSession.Status.DRAFT, ReviewSession.Status.COMPLETED]

        elif current_status == ReviewSession.Status.COMPLETED:
            if has_reviews:
                return []  # Cannot change status once completed with reviews
            else:
                return [ReviewSession.Status.DRAFT, ReviewSession.Status.REVIEWING]

        return []


class SequentialReviewWorkflow(ReviewWorkflow):
    """Workflow where reviews must be completed in a specific order."""

    def __init__(self, required_phases: List[str]):
        self.required_phases = required_phases

    def can_start_review(self, review_session: "ReviewSession") -> bool:
        """Check if a review session can be started."""
        # Add logic to check if previous phases are completed
        return review_session.status == review_session.Status.REVIEWING

    def can_see_recap(self, review_session: "ReviewSession") -> bool:
        """Check if recap can be viewed for this session."""
        # Only allow recap if all phases are completed
        return review_session.is_completed

    def get_allowed_status_transitions(
        self, current_status: str, has_reviews: bool
    ) -> List[str]:
        """Return allowed status transitions based on current state."""

        # Simplified for now - can be extended based on phase requirements
        return StandardReviewWorkflow().get_allowed_status_transitions(
            current_status, has_reviews
        )


class BlindReviewWorkflow(ReviewWorkflow):
    """Workflow for blind reviews where reviewers can't see other reviews."""

    def can_start_review(self, review_session: "ReviewSession") -> bool:
        """Check if a review session can be started."""
        return review_session.status == review_session.Status.REVIEWING

    def can_see_recap(self, review_session: "ReviewSession") -> bool:
        """Check if recap can be viewed for this session."""
        # Only allow recap after review phase is completed
        return review_session.is_completed

    def get_allowed_status_transitions(
        self, current_status: str, has_reviews: bool
    ) -> List[str]:
        """Return allowed status transitions based on current state."""
        from reviews.models import ReviewSession

        if current_status == ReviewSession.Status.DRAFT:
            return [ReviewSession.Status.REVIEWING]

        elif current_status == ReviewSession.Status.REVIEWING:
            return [ReviewSession.Status.COMPLETED]

        elif current_status == ReviewSession.Status.COMPLETED:
            return []  # No transitions allowed once completed

        return []


class ConditionalReviewWorkflow(ReviewWorkflow):
    """Workflow with conditional logic based on review session type."""

    def can_start_review(self, review_session: "ReviewSession") -> bool:
        """Check if a review session can be started."""
        if review_session.is_proposals_review:
            return review_session.status == review_session.Status.REVIEWING

        elif review_session.is_grants_review:
            # Grants can only be reviewed when session is in reviewing status
            return (
                review_session.status == review_session.Status.REVIEWING
                and review_session.can_review_items
            )

        return False

    def can_see_recap(self, review_session: "ReviewSession") -> bool:
        """Check if recap can be viewed for this session."""
        if review_session.is_proposals_review:
            return True

        if review_session.is_grants_review and review_session.is_completed:
            return True

        return False

    def get_allowed_status_transitions(
        self, current_status: str, has_reviews: bool
    ) -> List[str]:
        """Return allowed status transitions based on current state."""
        # Use standard workflow logic
        return StandardReviewWorkflow().get_allowed_status_transitions(
            current_status, has_reviews
        )
