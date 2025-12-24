from typing import List, Optional, TYPE_CHECKING

from reviews.interfaces import ScoringSystem

if TYPE_CHECKING:
    from reviews.models import UserReview


class StandardScoringSystem(ScoringSystem):
    """Standard scoring system using numeric scores."""

    def __init__(self, score_choices: Optional[List[tuple]] = None):
        self.score_choices = score_choices or [
            (-2, "Strongly Disagree"),
            (-1, "Disagree"),
            (0, "Neutral"),
            (1, "Agree"),
            (2, "Strongly Agree"),
        ]

    def get_score_choices(self) -> List[tuple]:
        """Return available score choices as (value, label) tuples."""
        return self.score_choices

    def calculate_aggregate_score(
        self, user_reviews: List["UserReview"]
    ) -> Optional[float]:
        """Calculate the average score from multiple user reviews."""
        if not user_reviews:
            return None

        scores = [review.score.numeric_value for review in user_reviews if review.score]
        return sum(scores) / len(scores) if scores else None

    def format_score_display(self, score: float) -> str:
        """Format a score for display in templates."""
        return f"{score:.1f}"


class WeightedScoringSystem(ScoringSystem):
    """Scoring system that allows different weights for different reviewers."""

    def __init__(
        self,
        score_choices: Optional[List[tuple]] = None,
        weights: Optional[dict] = None,
    ):
        self.score_choices = score_choices or [
            (-2, "Strongly Disagree"),
            (-1, "Disagree"),
            (0, "Neutral"),
            (1, "Agree"),
            (2, "Strongly Agree"),
        ]
        self.weights = weights or {}  # user_id -> weight

    def get_score_choices(self) -> List[tuple]:
        """Return available score choices as (value, label) tuples."""
        return self.score_choices

    def calculate_aggregate_score(
        self, user_reviews: List["UserReview"]
    ) -> Optional[float]:
        """Calculate weighted average score from multiple user reviews."""
        if not user_reviews:
            return None

        total_score = 0
        total_weight = 0

        for review in user_reviews:
            if review.score:
                weight = self.weights.get(review.user_id, 1.0)  # Default weight is 1.0
                total_score += review.score.numeric_value * weight
                total_weight += weight

        return total_score / total_weight if total_weight > 0 else None

    def format_score_display(self, score: float) -> str:
        """Format a score for display in templates."""
        return f"{score:.2f}"


class RankingScoringSystem(ScoringSystem):
    """Scoring system based on rankings rather than numeric scores."""

    def __init__(self):
        self.score_choices = [
            (1, "Top Choice"),
            (2, "Second Choice"),
            (3, "Third Choice"),
            (4, "Fourth Choice"),
            (5, "Fifth Choice"),
        ]

    def get_score_choices(self) -> List[tuple]:
        """Return available score choices as (value, label) tuples."""
        return self.score_choices

    def calculate_aggregate_score(
        self, user_reviews: List["UserReview"]
    ) -> Optional[float]:
        """Calculate average ranking (lower is better)."""
        if not user_reviews:
            return None

        rankings = [
            review.score.numeric_value for review in user_reviews if review.score
        ]
        return sum(rankings) / len(rankings) if rankings else None

    def format_score_display(self, score: float) -> str:
        """Format a ranking for display in templates."""
        return f"Rank {score:.1f}"


class BinaryScoringSystem(ScoringSystem):
    """Simple binary scoring system (Accept/Reject)."""

    def __init__(self):
        self.score_choices = [
            (0, "Reject"),
            (1, "Accept"),
        ]

    def get_score_choices(self) -> List[tuple]:
        """Return available score choices as (value, label) tuples."""
        return self.score_choices

    def calculate_aggregate_score(
        self, user_reviews: List["UserReview"]
    ) -> Optional[float]:
        """Calculate percentage of acceptances."""
        if not user_reviews:
            return None

        scores = [review.score.numeric_value for review in user_reviews if review.score]
        return sum(scores) / len(scores) if scores else None

    def format_score_display(self, score: float) -> str:
        """Format a binary score as percentage."""
        return f"{score * 100:.0f}% acceptance"
