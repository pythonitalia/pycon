import factory
import factory.fuzzy
from conferences.tests.factories import ConferenceFactory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from sponsors.models import Sponsor, SponsorLevel


@register
class SponsorLevelFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    name = factory.Faker("word")

    class Meta:
        model = SponsorLevel


@register
class SponsorFactory(DjangoModelFactory):
    level = factory.SubFactory(SponsorLevelFactory)
    name = factory.Faker("word")
    image = factory.django.ImageField()
    order = factory.Faker("pyint", min_value=0)

    class Meta:
        model = Sponsor
