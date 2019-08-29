import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pages.models import Page
from pytest_factoryboy import register
from tests.conferences.factories import ConferenceFactory


@register
class PageFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    title = factory.Faker("sentence")
    slug = factory.Faker("slug")
    content = factory.Faker("sentence")
    published = True
    image = factory.django.ImageField()

    class Meta:
        model = Page
