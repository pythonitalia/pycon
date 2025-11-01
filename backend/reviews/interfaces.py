from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, TYPE_CHECKING

from django.db import models
from django.http import HttpRequest

if TYPE_CHECKING:
    from reviews.models import ReviewSession, UserReview
    from users.models import User


class ReviewableItem(Protocol):
    """Protocol for items that can be reviewed."""

    id: int

    def get_review_display_name(self) -> str:
        """Return a human-readable name for the item being reviewed."""
        ...

    def get_review_context_data(self, request: HttpRequest) -> Dict[str, Any]:
        """Return context data specific to this item type for review templates."""
        ...

    def can_be_reviewed_by(self, user: "User") -> bool:
        """Check if the given user can review this item."""
        ...


class ReviewStrategy(ABC):
    """Abstract strategy for handling different review workflows."""

    @abstractmethod
    def get_reviewable_items_queryset(
        self, review_session: "ReviewSession"
    ) -> models.QuerySet:
        """Return a queryset of items that can be reviewed in this session."""

    @abstractmethod
    def get_next_item_to_review(
        self,
        review_session: "ReviewSession",
        user: "User",
        skip_item: Optional[int] = None,
        exclude: Optional[List[int]] = None,
        seen: Optional[List[int]] = None,
    ) -> Optional[int]:
        """Find the next item ID to review for the given user."""

    @abstractmethod
    def get_review_template_name(self) -> str:
        """Return the template name for reviewing items of this type."""

    @abstractmethod
    def get_recap_template_name(self) -> str:
        """Return the template name for the recap view of this review type."""

    @abstractmethod
    def process_review_decisions(
        self, request: HttpRequest, review_session: "ReviewSession"
    ) -> None:
        """Process decisions made during the review recap phase."""

    @abstractmethod
    def get_recap_context_data(
        self, request: HttpRequest, review_session: "ReviewSession"
    ) -> Dict[str, Any]:
        """Return context data for the recap template."""

    @abstractmethod
    def validate_user_review_data(self, data: Dict[str, Any]) -> bool:
        """Validate the data submitted for a user review."""

    @abstractmethod
    def create_user_review_fields(self, review_item_id: int) -> Dict[str, Any]:
        """Create the fields needed for a UserReview based on the item type."""


class ScoringSystem(ABC):
    """Abstract base class for different scoring systems."""

    @abstractmethod
    def get_score_choices(self) -> List[tuple]:
        """Return available score choices as (value, label) tuples."""

    @abstractmethod
    def calculate_aggregate_score(
        self, user_reviews: List["UserReview"]
    ) -> Optional[float]:
        """Calculate an aggregate score from multiple user reviews."""

    @abstractmethod
    def format_score_display(self, score: float) -> str:
        """Format a score for display in templates."""


class ReviewWorkflow(ABC):
    """Abstract base class for review workflow management."""

    @abstractmethod
    def can_start_review(self, review_session: "ReviewSession") -> bool:
        """Check if a review session can be started."""

    @abstractmethod
    def can_see_recap(self, review_session: "ReviewSession") -> bool:
        """Check if recap can be viewed for this session."""

    @abstractmethod
    def get_allowed_status_transitions(
        self, current_status: str, has_reviews: bool
    ) -> List[str]:
        """Return allowed status transitions based on current state."""
