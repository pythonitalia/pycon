import factory
import factory.fuzzy
from conferences.tests.factories import ConferenceFactory
from factory.django import DjangoModelFactory
from i18n.tests.factories import LanguageFactory
from pytest_factoryboy import register

from ..models import Event


@register
class EventFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    title = LanguageFactory("sentence")
    slug = LanguageFactory("slug")
    content = LanguageFactory("text")
    image = factory.django.ImageField()

    class Meta:
        model = Event
