import factory
import factory.fuzzy
from conferences.tests.factories import ConferenceFactory
from factory.django import DjangoModelFactory
from i18n.helpers.tests import LanguageFactory
from pages.models import Page
from pytest_factoryboy import register


@register
class PageFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    factory.Faker
    title = LanguageFactory("sentence")
    slug = LanguageFactory("slug")
    content = LanguageFactory("sentence")
    published = True
    image = factory.django.ImageField()

    class Meta:
        model = Page
