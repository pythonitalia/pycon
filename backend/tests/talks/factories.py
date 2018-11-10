import factory

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from tests.conferences.factories import ConferenceFactory

from talks.models import Talk


@register
class TalkFactory(DjangoModelFactory):
    class Meta:
        model = Talk

    conference = factory.SubFactory(ConferenceFactory)

    title = factory.Faker('sentence')
    abstract = factory.Faker('paragraphs')
