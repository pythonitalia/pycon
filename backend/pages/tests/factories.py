import factory
import factory.fuzzy
from conferences.tests.factories import ConferenceFactory
from factory.django import DjangoModelFactory
from pages.models import Page
from pytest_factoryboy import register


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
