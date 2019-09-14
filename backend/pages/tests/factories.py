import factory
import factory.fuzzy
from django.conf import settings
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from i18n.strings import LazyI18nString
from pages.models import Page


class LanguageFactory(factory.Faker):
    def generate(self, extra_kwargs=None):
        kwargs = {}
        kwargs.update(self.provider_kwargs)
        kwargs.update(extra_kwargs or {})

        locale_to_faker = {"en": "en_US", "it": "it_IT"}

        data = {}

        for lang, _ in settings.LANGUAGES:
            fake = self._get_faker(locale_to_faker[lang])
            data[lang] = fake.format(self.provider, **kwargs)

        return LazyI18nString(data)


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
