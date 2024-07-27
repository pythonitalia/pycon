import factory
import factory.fuzzy
from cms.models import FAQ, GenericCopy, Menu, MenuLink
from conferences.tests.factories import ConferenceFactory
from factory.django import DjangoModelFactory
from i18n.tests.factories import LanguageFactory


class GenericCopyFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    key = factory.Faker("slug")
    content = LanguageFactory("sentence")

    class Meta:
        model = GenericCopy


class FAQFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    question = LanguageFactory("sentence")
    answer = LanguageFactory("sentence")

    class Meta:
        model = FAQ


class MenuFactory(DjangoModelFactory):
    title = LanguageFactory("sentence")
    conference = factory.SubFactory(ConferenceFactory)
    identifier = factory.Faker("slug")

    class Meta:
        model = Menu


class MenuLinkFactory(DjangoModelFactory):
    menu = factory.SubFactory(MenuFactory)
    title = LanguageFactory("sentence")
    href = LanguageFactory("slug")

    class Meta:
        model = MenuLink
