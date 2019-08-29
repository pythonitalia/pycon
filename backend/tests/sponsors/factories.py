import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from sponsors.models import Sponsor
from tests.conferences.factories import ConferenceFactory


@register
class SponsorFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    name = factory.Faker("word")
    level = factory.Faker("word")
    image = factory.django.ImageField()

    class Meta:
        model = Sponsor
