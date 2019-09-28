import factory
import factory.fuzzy
from cms.models import FAQ, GenericCopy
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


@register
class FAQFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    question = LanguageFactory("sentence")
    answer = LanguageFactory("sentence")

    class Meta:
        model = FAQ
