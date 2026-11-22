import pytest
from django.contrib.auth.models import Permission

from reviews.models import ReviewSession
from reviews.tests.factories import AvailableScoreOptionFactory, ReviewSessionFactory
from users.tests.factories import UserFactory


@pytest.fixture
def make_reviewer():
    def _make_reviewer(conference):
        user = UserFactory(is_staff=True)
        user.admin_conferences.add(conference)
        user.user_permissions.add(
            *Permission.objects.filter(
                codename__in=["review_reviewsession", "view_submission"]
            )
        )
        return user

    return _make_reviewer


@pytest.fixture
def proposals_review_session():
    review_session = ReviewSessionFactory(
        session_type=ReviewSession.SessionType.PROPOSALS
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)
    return review_session
