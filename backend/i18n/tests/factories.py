import faker
import factory
from django.conf import settings
from i18n.strings import LazyI18nString


class LanguageFactory(factory.fuzzy.BaseFuzzyAttribute):
    _registry = {}

    def __init__(self, provider, extra_kwargs=None, defaults=None):
        self.provider = provider
        self.extra_kwargs = extra_kwargs or {}
        self._defaults = defaults or {}

    def fuzz(self):
        data = {}

        for lang, _ in settings.LANGUAGES:
            fake = self.get_faker(lang)
            data[lang] = fake.format(self.provider, **self.extra_kwargs)

        return LazyI18nString(data)

    @classmethod
    def get_faker(cls, lang):
        locale_to_faker = {"en": "en_US", "it": "it_IT"}
        locale = locale_to_faker[lang]

        if locale in cls._registry:
            return cls._registry[locale]

        cls._registry[locale] = faker.Faker(locale=locale)
        return cls._registry[locale]
