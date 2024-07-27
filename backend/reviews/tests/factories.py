import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from conferences.tests.factories import ConferenceFactory
from reviews.models import AvailableScoreOption, ReviewSession, UserReview


class ReviewSessionFactory(DjangoModelFactory):
    class Meta:
        model = ReviewSession

    session_type = factory.fuzzy.FuzzyChoice(["proposals", "grants"])
    conference = factory.SubFactory(ConferenceFactory)


class UserReviewFactory(DjangoModelFactory):
    class Meta:
        model = UserReview

    review_session = factory.SubFactory(ReviewSessionFactory)
    proposal = None
    grant = None


class AvailableScoreOptionFactory(DjangoModelFactory):
    class Meta:
        model = AvailableScoreOption

    review_session = factory.SubFactory(ReviewSessionFactory)
    numeric_value = factory.fuzzy.FuzzyInteger(1, 5)
    label = factory.Faker("slug")
