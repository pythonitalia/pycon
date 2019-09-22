import factory
import factory.fuzzy
from cms.models import GenericCopy
from conferences.tests.factories import ConferenceFactory
from factory.django import DjangoModelFactory
from i18n.helpers.tests import LanguageFactory
from pytest_factoryboy import register


@register
class GenericCopyFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    key = factory.Faker("slug")
    content = LanguageFactory("sentence")

    class Meta:
        model = GenericCopy
