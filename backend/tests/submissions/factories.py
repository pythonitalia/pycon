import factory

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from tests.conferences.factories import ConferenceFactory, DurationFactory

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
