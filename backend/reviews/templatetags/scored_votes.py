from collections.abc import Iterable

from django import template

from reviews.models import UserReview

register = template.Library()


@register.filter
def scored_votes(user_reviews: Iterable[UserReview]) -> int:
    return sum(1 for user_review in user_reviews if user_review.score_id is not None)
