import pytest
from django.test import RequestFactory

from conferences.tests.factories import ConferenceFactory
from grants.tests.factories import GrantFactory
from reviews.models import ReviewSession
from reviews.services import ReviewSessionService, ReviewItemService, ReviewVoteService
from reviews.tests.factories import (
    AvailableScoreOptionFactory,
    ReviewSessionFactory,
    UserReviewFactory,
)
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestReviewSessionService:
    """Test ReviewSessionService functionality."""

    def test_can_user_review(self):
        user = UserFactory(is_staff=True, is_superuser=True)
        review_session = ReviewSessionFactory(
            session_type=ReviewSession.SessionType.PROPOSALS
        )

        service = ReviewSessionService(review_session)
        result = service.can_user_review(user)

        assert result is True

    def test_get_next_item_to_review_for_proposals(self):
        user = UserFactory(is_staff=True, is_superuser=True)
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference,
            session_type=ReviewSession.SessionType.PROPOSALS,
        )

        submission_1 = SubmissionFactory(conference=conference)
        submission_2 = SubmissionFactory(conference=conference)

        service = ReviewSessionService(review_session)
        next_item = service.get_next_item_to_review(user)

        assert next_item in [submission_1.id, submission_2.id]

    def test_get_next_item_to_review_for_grants(self):
        user = UserFactory(is_staff=True, is_superuser=True)
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference,
            session_type=ReviewSession.SessionType.GRANTS,
        )

        grant_1 = GrantFactory(conference=conference)
        grant_2 = GrantFactory(conference=conference)

        service = ReviewSessionService(review_session)
        next_item = service.get_next_item_to_review(user)

        assert next_item in [grant_1.id, grant_2.id]

    def test_next_item_prefers_items_with_fewer_votes(self):
        user_1 = UserFactory(is_staff=True, is_superuser=True)
        user_2 = UserFactory(is_staff=True, is_superuser=True)
        conference = ConferenceFactory()

        review_session = ReviewSessionFactory(
            conference=conference,
            session_type=ReviewSession.SessionType.PROPOSALS,
        )
        score = AvailableScoreOptionFactory(
            review_session=review_session, numeric_value=0
        )

        submission_1 = SubmissionFactory(conference=conference)
        submission_2 = SubmissionFactory(conference=conference)

        # Give submission_1 a review
        UserReviewFactory(
            review_session=review_session,
            proposal=submission_1,
            user=user_1,
            score=score,
        )

        service = ReviewSessionService(review_session)
        next_item = service.get_next_item_to_review(user_2)

        # Should prefer submission_2 which has no reviews
        assert next_item == submission_2.id


class TestReviewItemService:
    """Test ReviewItemService functionality."""

    def test_get_review_template_name_for_proposals(self):
        review_session = ReviewSessionFactory(
            session_type=ReviewSession.SessionType.PROPOSALS
        )

        service = ReviewItemService(review_session)
        template_name = service.get_review_template_name()

        assert template_name == "reviews/proposal-review.html"

    def test_get_review_template_name_for_grants(self):
        review_session = ReviewSessionFactory(
            session_type=ReviewSession.SessionType.GRANTS
        )

        service = ReviewItemService(review_session)
        template_name = service.get_review_template_name()

        assert template_name == "reviews/grant-review.html"

    def test_get_recap_template_name(self):
        review_session = ReviewSessionFactory(
            session_type=ReviewSession.SessionType.PROPOSALS
        )

        service = ReviewItemService(review_session)
        template_name = service.get_recap_template_name()

        assert template_name == "proposals-recap.html"

    def test_get_item_context_data_for_proposal(self):
        rf = RequestFactory()
        request = rf.get("/")

        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference, session_type=ReviewSession.SessionType.PROPOSALS
        )
        submission = SubmissionFactory(conference=conference)

        service = ReviewItemService(review_session)
        context = service.get_item_context_data(request, submission.id)

        assert "proposal" in context
        assert "available_scores" in context
        assert "review_session_id" in context

    def test_get_item_context_data_for_grant(self):
        rf = RequestFactory()
        request = rf.get("/")

        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference, session_type=ReviewSession.SessionType.GRANTS
        )
        grant = GrantFactory(conference=conference)

        service = ReviewItemService(review_session)
        context = service.get_item_context_data(request, grant.id)

        assert "grant" in context
        assert "available_scores" in context
        assert "review_session_id" in context


class TestReviewVoteService:
    """Test ReviewVoteService functionality."""

    def test_process_vote_submission_with_next(self):
        user = UserFactory(is_staff=True, is_superuser=True)
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference,
            session_type=ReviewSession.SessionType.PROPOSALS,
        )
        score = AvailableScoreOptionFactory(
            review_session=review_session, numeric_value=1
        )

        submission_1 = SubmissionFactory(conference=conference)
        submission_2 = SubmissionFactory(conference=conference)

        rf = RequestFactory()
        request = rf.post("/")
        request.user = user

        service = ReviewVoteService(review_session)
        form_data = {
            "score": score,
            "comment": "Good proposal",
            "private_comment": "Private note",
            "_next": True,
            "seen": "",
            "exclude": [],
        }

        next_item = service.process_vote_submission(request, submission_1.id, form_data)

        # Should return the next item to review
        assert next_item == submission_2.id

        # Should have created a UserReview
        from reviews.models import UserReview

        review = UserReview.objects.filter(
            user=user, review_session=review_session, proposal=submission_1
        ).first()

        assert review is not None
        assert review.score == score
        assert review.comment == "Good proposal"
        assert review.private_comment == "Private note"

    def test_process_vote_submission_with_skip(self):
        user = UserFactory(is_staff=True, is_superuser=True)
        conference = ConferenceFactory()
        review_session = ReviewSessionFactory(
            conference=conference,
            session_type=ReviewSession.SessionType.PROPOSALS,
        )

        submission_1 = SubmissionFactory(conference=conference)
        submission_2 = SubmissionFactory(conference=conference)

        rf = RequestFactory()
        request = rf.post("/")
        request.user = user

        service = ReviewVoteService(review_session)
        form_data = {
            "_skip": True,
            "seen": "",
            "exclude": [],
        }

        next_item = service.process_vote_submission(request, submission_1.id, form_data)

        # Should return the next item to review
        assert next_item == submission_2.id

        # Should NOT have created a UserReview
        from reviews.models import UserReview

        review_count = UserReview.objects.filter(
            user=user, review_session=review_session, proposal=submission_1
        ).count()

        assert review_count == 0
