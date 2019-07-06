import factory
import factory.fuzzy

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from tests.conferences.factories import ConferenceFactory, DurationFactory, \
    TopicFactory, AudienceLevelFactory
from tests.languages.factories import LanguageFactory
from tests.users.factories import UserFactory

from submissions.models import Submission, SubmissionType


@register
class SubmissionTypeFactory(DjangoModelFactory):
    class Meta:
        model = SubmissionType
        django_get_or_create = ('name', )

    name = factory.fuzzy.FuzzyChoice(['talk', 'tutorial'])


@register
class SubmissionFactory(DjangoModelFactory):
    class Meta:
        model = Submission

    conference = factory.SubFactory(ConferenceFactory)

    title = factory.Faker('sentence')
    abstract = factory.Faker('text')
    elevator_pitch = factory.Faker('text')
    notes = factory.Faker('text')
    type = factory.SubFactory(SubmissionTypeFactory)
    duration = factory.SubFactory(DurationFactory)
    language = factory.SubFactory(LanguageFactory)
    speaker = factory.SubFactory(UserFactory)
    topic = factory.SubFactory(TopicFactory)
    audience_level = factory.SubFactory(AudienceLevelFactory)
