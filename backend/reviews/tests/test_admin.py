import pytest
from users.tests.factories import UserFactory

from reviews.admin import get_next_to_review_item_id
from reviews.models import ReviewSession

pytestmark = pytest.mark.django_db


def test_next_item_to_review_prefers_items_with_fewer_votes(
    review_session_factory,
    available_score_option_factory,
    user_review_factory,
    submission_factory,
    conference_factory,
    submission_tag_factory,
):
    tag = submission_tag_factory()

    user_1 = UserFactory(is_staff=True, is_superuser=True)
    user_2 = UserFactory(is_staff=True, is_superuser=True)

    conference = conference_factory()

    review_session = review_session_factory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
    )
    score_0 = available_score_option_factory(
        review_session=review_session, numeric_value=0
    )
    available_score_option_factory(review_session=review_session, numeric_value=1)

    submission_1 = submission_factory(conference=conference)
    submission_1.tags.add(tag)
    submission_2 = submission_factory(conference=conference)
    submission_2.tags.add(tag)

    user_review_factory(
        review_session=review_session,
        proposal=submission_1,
        user=user_1,
        score=score_0,
    )

    next_to_review = get_next_to_review_item_id(review_session, user_2)
    assert next_to_review == submission_2.id
