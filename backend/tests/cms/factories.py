import factory
import factory.fuzzy
from cms.models import GenericCopy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from tests.conferences.factories import ConferenceFactory


@register
class GenericCopyFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    key = factory.Faker("slug")
    content = factory.Faker("sentence")

    class Meta:
        model = GenericCopy
