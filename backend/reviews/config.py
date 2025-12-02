from typing import Dict, List, Optional, Type
from dataclasses import dataclass

from reviews.interfaces import ReviewStrategy, ScoringSystem, ReviewWorkflow

# Configuration for default review types
from reviews.strategies import ProposalReviewStrategy, GrantReviewStrategy
from reviews.scoring import StandardScoringSystem
from reviews.workflows import StandardReviewWorkflow


@dataclass
class ReviewSessionConfig:
    """Configuration for a review session type."""

    name: str
    strategy_class: Type[ReviewStrategy]
    scoring_system_class: Type[ScoringSystem]
    workflow_class: Type[ReviewWorkflow]

    # Permission settings
    review_permission: str = "reviews.review_reviewsession"
    decision_permission: str = "reviews.decision_reviewsession"

    # Template overrides
    review_template: Optional[str] = None
    recap_template: Optional[str] = None

    # Workflow settings
    allow_skip: bool = True
    allow_private_comments: bool = True
    require_comments: bool = False

    # Scoring settings
    default_score_options: Optional[List[tuple]] = None
    allow_custom_scores: bool = True


class ReviewSystemRegistry:
    """Registry for review session configurations."""

    def __init__(self):
        self._configs: Dict[str, ReviewSessionConfig] = {}
        self._strategies: Dict[str, Type[ReviewStrategy]] = {}
        self._scoring_systems: Dict[str, Type[ScoringSystem]] = {}
        self._workflows: Dict[str, Type[ReviewWorkflow]] = {}

    def register_config(self, session_type: str, config: ReviewSessionConfig) -> None:
        """Register a configuration for a session type."""
        self._configs[session_type] = config

    def register_strategy(
        self, name: str, strategy_class: Type[ReviewStrategy]
    ) -> None:
        """Register a review strategy."""
        self._strategies[name] = strategy_class

    def register_scoring_system(
        self, name: str, scoring_class: Type[ScoringSystem]
    ) -> None:
        """Register a scoring system."""
        self._scoring_systems[name] = scoring_class

    def register_workflow(
        self, name: str, workflow_class: Type[ReviewWorkflow]
    ) -> None:
        """Register a workflow."""
        self._workflows[name] = workflow_class

    def get_config(self, session_type: str) -> Optional[ReviewSessionConfig]:
        """Get configuration for a session type."""
        return self._configs.get(session_type)

    def get_strategy(self, name: str) -> Optional[Type[ReviewStrategy]]:
        """Get a strategy class by name."""
        return self._strategies.get(name)

    def get_scoring_system(self, name: str) -> Optional[Type[ScoringSystem]]:
        """Get a scoring system class by name."""
        return self._scoring_systems.get(name)

    def get_workflow(self, name: str) -> Optional[Type[ReviewWorkflow]]:
        """Get a workflow class by name."""
        return self._workflows.get(name)

    def list_session_types(self) -> List[str]:
        """List all registered session types."""
        return list(self._configs.keys())


# Global registry instance
registry = ReviewSystemRegistry()


def setup_default_configurations():
    """Set up default configurations for built-in review types."""

    # Register default components
    registry.register_strategy("proposal", ProposalReviewStrategy)
    registry.register_strategy("grant", GrantReviewStrategy)
    registry.register_scoring_system("standard", StandardScoringSystem)
    registry.register_workflow("standard", StandardReviewWorkflow)

    # Proposals configuration
    proposals_config = ReviewSessionConfig(
        name="Proposals Review",
        strategy_class=ProposalReviewStrategy,
        scoring_system_class=StandardScoringSystem,
        workflow_class=StandardReviewWorkflow,
        review_permission="reviews.review_reviewsession",
        decision_permission="reviews.decision_reviewsession",
        allow_skip=True,
        allow_private_comments=True,
        require_comments=False,
        default_score_options=[
            (-2, "Rejected"),
            (-1, "Not Convinced"),
            (0, "Maybe"),
            (1, "Good"),
            (2, "Excellent"),
        ],
    )

    # Grants configuration
    grants_config = ReviewSessionConfig(
        name="Grants Review",
        strategy_class=GrantReviewStrategy,
        scoring_system_class=StandardScoringSystem,
        workflow_class=StandardReviewWorkflow,
        review_permission="reviews.review_reviewsession",
        decision_permission="reviews.decision_reviewsession",
        allow_skip=True,
        allow_private_comments=True,
        require_comments=False,
        default_score_options=[
            (-2, "Rejected"),
            (-1, "Not Convinced"),
            (0, "Maybe"),
            (1, "Yes"),
            (2, "Absolutely"),
        ],
    )

    registry.register_config("proposals", proposals_config)
    registry.register_config("grants", grants_config)


# Auto-setup when module is imported
setup_default_configurations()
