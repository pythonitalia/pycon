import pytest

from conferences.tests.factories import ConferenceFactory
from grants.tests.factories import GrantFactory
from reviews.models import ReviewSession
from reviews.strategies import (
    ProposalReviewStrategy,
    GrantReviewStrategy,
    ReviewStrategyFactory,
)
from reviews.tests.factories import (
    ReviewSessionFactory,
)
from submissions.tests.factories import SubmissionFactory, SubmissionTagFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestProposalReviewStrategy:
    """Test ProposalReviewStrategy functionality."""

    def test_get_reviewable_items_queryset(self):
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference, session_type=ReviewSession.SessionType.PROPOSALS
        )

        submission_1 = SubmissionFactory(conference=conference)
        submission_2 = SubmissionFactory(conference=conference)
        # Create submission for different conference
        other_submission = SubmissionFactory()

        strategy = ProposalReviewStrategy()
        qs = strategy.get_reviewable_items_queryset(review_session)

        submission_ids = list(qs.values_list("id", flat=True))
        assert submission_1.id in submission_ids
        assert submission_2.id in submission_ids
        assert other_submission.id not in submission_ids

    def test_get_next_item_to_review(self):
        user = UserFactory(is_staff=True, is_superuser=True)
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference, session_type=ReviewSession.SessionType.PROPOSALS
        )

        submission_1 = SubmissionFactory(conference=conference)
        submission_2 = SubmissionFactory(conference=conference)

        strategy = ProposalReviewStrategy()
        next_item = strategy.get_next_item_to_review(review_session, user)

        assert next_item in [submission_1.id, submission_2.id]

    def test_get_next_item_excludes_tags(self):
        user = UserFactory(is_staff=True, is_superuser=True)
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference, session_type=ReviewSession.SessionType.PROPOSALS
        )

        tag_1 = SubmissionTagFactory()
        tag_2 = SubmissionTagFactory()

        submission_1 = SubmissionFactory(conference=conference)
        submission_1.tags.add(tag_1)

        submission_2 = SubmissionFactory(conference=conference)
        submission_2.tags.add(tag_2)

        strategy = ProposalReviewStrategy()
        next_item = strategy.get_next_item_to_review(
            review_session, user, exclude=[tag_1.id]
        )

        assert next_item == submission_2.id

    def test_get_template_names(self):
        strategy = ProposalReviewStrategy()

        assert strategy.get_review_template_name() == "reviews/proposal-review.html"
        assert strategy.get_recap_template_name() == "proposals-recap.html"

    def test_validate_user_review_data(self):
        strategy = ProposalReviewStrategy()

        valid_data = {"score": "some_score"}
        invalid_data = {"comment": "no score"}

        assert strategy.validate_user_review_data(valid_data) is True
        assert strategy.validate_user_review_data(invalid_data) is False

    def test_create_user_review_fields(self):
        strategy = ProposalReviewStrategy()
        fields = strategy.create_user_review_fields(123)

        assert fields == {"proposal_id": 123}


class TestGrantReviewStrategy:
    """Test GrantReviewStrategy functionality."""

    def test_get_reviewable_items_queryset(self):
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference, session_type=ReviewSession.SessionType.GRANTS
        )

        grant_1 = GrantFactory(conference=conference)
        grant_2 = GrantFactory(conference=conference)
        # Create grant for different conference
        other_grant = GrantFactory()

        strategy = GrantReviewStrategy()
        qs = strategy.get_reviewable_items_queryset(review_session)

        grant_ids = list(qs.values_list("id", flat=True))
        assert grant_1.id in grant_ids
        assert grant_2.id in grant_ids
        assert other_grant.id not in grant_ids

    def test_get_next_item_to_review(self):
        user = UserFactory(is_staff=True, is_superuser=True)
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference, session_type=ReviewSession.SessionType.GRANTS
        )

        grant_1 = GrantFactory(conference=conference)
        grant_2 = GrantFactory(conference=conference)

        strategy = GrantReviewStrategy()
        next_item = strategy.get_next_item_to_review(review_session, user)

        assert next_item in [grant_1.id, grant_2.id]

    def test_get_template_names(self):
        strategy = GrantReviewStrategy()

        assert strategy.get_review_template_name() == "reviews/grant-review.html"
        assert strategy.get_recap_template_name() == "grants-recap.html"

    def test_validate_user_review_data(self):
        strategy = GrantReviewStrategy()

        valid_data = {"score": "some_score"}
        invalid_data = {"comment": "no score"}

        assert strategy.validate_user_review_data(valid_data) is True
        assert strategy.validate_user_review_data(invalid_data) is False

    def test_create_user_review_fields(self):
        strategy = GrantReviewStrategy()
        fields = strategy.create_user_review_fields(456)

        assert fields == {"grant_id": 456}


class TestReviewStrategyFactory:
    """Test ReviewStrategyFactory functionality."""

    def test_get_strategy_for_proposals(self):
        strategy = ReviewStrategyFactory.get_strategy(
            ReviewSession.SessionType.PROPOSALS
        )

        assert isinstance(strategy, ProposalReviewStrategy)

    def test_get_strategy_for_grants(self):
        strategy = ReviewStrategyFactory.get_strategy(ReviewSession.SessionType.GRANTS)

        assert isinstance(strategy, GrantReviewStrategy)

    def test_get_strategy_for_unknown_type(self):
        with pytest.raises(ValueError, match="No strategy found for session type"):
            ReviewStrategyFactory.get_strategy("unknown_type")

    def test_register_custom_strategy(self):
        class CustomStrategy(ProposalReviewStrategy):
            pass

        ReviewStrategyFactory.register_strategy("custom", CustomStrategy)
        strategy = ReviewStrategyFactory.get_strategy("custom")

        assert isinstance(strategy, CustomStrategy)

        # Clean up
        ReviewStrategyFactory._strategies.pop("custom", None)
