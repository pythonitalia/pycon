import factory
import factory.fuzzy
from conferences.tests.factories import (
    AudienceLevelFactory,
    ConferenceFactory,
    DurationFactory,
    TopicFactory,
)
from factory.django import DjangoModelFactory
from languages.tests.factories import LanguageFactory
from pytest_factoryboy import register
from submissions.models import Submission, SubmissionType
from users.tests.factories import UserFactory


@register
class SubmissionTypeFactory(DjangoModelFactory):
    class Meta:
        model = SubmissionType
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(["talk", "tutorial"])


@register
class SubmissionFactory(DjangoModelFactory):
    class Meta:
        model = Submission

    conference = factory.SubFactory(ConferenceFactory)

    title = factory.Faker("sentence")
    abstract = factory.Faker("text")
    elevator_pitch = factory.Faker("text")
    notes = factory.Faker("text")
    type = factory.SubFactory(SubmissionTypeFactory)
    duration = factory.SubFactory(DurationFactory)
    language = factory.SubFactory(LanguageFactory)
    speaker = factory.SubFactory(UserFactory)
    topic = factory.SubFactory(TopicFactory)
    audience_level = factory.SubFactory(AudienceLevelFactory)
