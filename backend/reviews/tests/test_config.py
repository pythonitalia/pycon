from reviews.config import ReviewSessionConfig, ReviewSystemRegistry
from reviews.strategies import ProposalReviewStrategy, GrantReviewStrategy
from reviews.scoring import StandardScoringSystem
from reviews.workflows import StandardReviewWorkflow


class TestReviewSessionConfig:
    """Test ReviewSessionConfig dataclass."""

    def test_create_config_with_defaults(self):
        config = ReviewSessionConfig(
            name="Test Review",
            strategy_class=ProposalReviewStrategy,
            scoring_system_class=StandardScoringSystem,
            workflow_class=StandardReviewWorkflow,
        )

        assert config.name == "Test Review"
        assert config.strategy_class == ProposalReviewStrategy
        assert config.scoring_system_class == StandardScoringSystem
        assert config.workflow_class == StandardReviewWorkflow
        assert config.review_permission == "reviews.review_reviewsession"
        assert config.decision_permission == "reviews.decision_reviewsession"
        assert config.allow_skip is True
        assert config.allow_private_comments is True
        assert config.require_comments is False

    def test_create_config_with_custom_settings(self):
        config = ReviewSessionConfig(
            name="Custom Review",
            strategy_class=ProposalReviewStrategy,
            scoring_system_class=StandardScoringSystem,
            workflow_class=StandardReviewWorkflow,
            allow_skip=False,
            require_comments=True,
            default_score_options=[(0, "Bad"), (1, "Good")],
        )

        assert config.allow_skip is False
        assert config.require_comments is True
        assert config.default_score_options == [(0, "Bad"), (1, "Good")]


class TestReviewSystemRegistry:
    """Test ReviewSystemRegistry functionality."""

    def test_register_and_get_config(self):
        registry = ReviewSystemRegistry()

        config = ReviewSessionConfig(
            name="Test Review",
            strategy_class=ProposalReviewStrategy,
            scoring_system_class=StandardScoringSystem,
            workflow_class=StandardReviewWorkflow,
        )

        registry.register_config("test", config)
        retrieved_config = registry.get_config("test")

        assert retrieved_config == config

    def test_get_nonexistent_config(self):
        registry = ReviewSystemRegistry()
        config = registry.get_config("nonexistent")

        assert config is None

    def test_register_and_get_strategy(self):
        registry = ReviewSystemRegistry()

        registry.register_strategy("test_strategy", ProposalReviewStrategy)
        strategy_class = registry.get_strategy("test_strategy")

        assert strategy_class == ProposalReviewStrategy

    def test_register_and_get_scoring_system(self):
        registry = ReviewSystemRegistry()

        registry.register_scoring_system("test_scoring", StandardScoringSystem)
        scoring_class = registry.get_scoring_system("test_scoring")

        assert scoring_class == StandardScoringSystem

    def test_register_and_get_workflow(self):
        registry = ReviewSystemRegistry()

        registry.register_workflow("test_workflow", StandardReviewWorkflow)
        workflow_class = registry.get_workflow("test_workflow")

        assert workflow_class == StandardReviewWorkflow

    def test_list_session_types(self):
        registry = ReviewSystemRegistry()

        config1 = ReviewSessionConfig(
            name="Test Review 1",
            strategy_class=ProposalReviewStrategy,
            scoring_system_class=StandardScoringSystem,
            workflow_class=StandardReviewWorkflow,
        )

        config2 = ReviewSessionConfig(
            name="Test Review 2",
            strategy_class=GrantReviewStrategy,
            scoring_system_class=StandardScoringSystem,
            workflow_class=StandardReviewWorkflow,
        )

        registry.register_config("test1", config1)
        registry.register_config("test2", config2)

        session_types = registry.list_session_types()

        assert "test1" in session_types
        assert "test2" in session_types
        assert len(session_types) == 2


class TestDefaultConfigurations:
    """Test that default configurations are set up correctly."""

    def test_default_registry_has_configurations(self):
        from reviews.config import registry

        # Check that default session types are registered
        session_types = registry.list_session_types()
        assert "proposals" in session_types
        assert "grants" in session_types

    def test_proposals_config(self):
        from reviews.config import registry

        config = registry.get_config("proposals")

        assert config is not None
        assert config.name == "Proposals Review"
        assert config.strategy_class == ProposalReviewStrategy
        assert config.scoring_system_class == StandardScoringSystem
        assert config.workflow_class == StandardReviewWorkflow

    def test_grants_config(self):
        from reviews.config import registry

        config = registry.get_config("grants")

        assert config is not None
        assert config.name == "Grants Review"
        assert config.strategy_class == GrantReviewStrategy
        assert config.scoring_system_class == StandardScoringSystem
        assert config.workflow_class == StandardReviewWorkflow

    def test_default_strategies_registered(self):
        from reviews.config import registry

        proposal_strategy = registry.get_strategy("proposal")
        grant_strategy = registry.get_strategy("grant")

        assert proposal_strategy == ProposalReviewStrategy
        assert grant_strategy == GrantReviewStrategy

    def test_default_scoring_systems_registered(self):
        from reviews.config import registry

        scoring_system = registry.get_scoring_system("standard")

        assert scoring_system == StandardScoringSystem

    def test_default_workflows_registered(self):
        from reviews.config import registry

        workflow = registry.get_workflow("standard")

        assert workflow == StandardReviewWorkflow
