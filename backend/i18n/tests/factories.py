import factory
from django.conf import settings
from i18n.strings import LazyI18nString


class LanguageFactory(factory.Faker):
    def generate(self, extra_kwargs=None):
        kwargs = {}
        kwargs.update(extra_kwargs or {})
        kwargs.pop("locale")

        locale_to_faker = {"en": "en_US", "it": "it_IT"}

        data = {}

        for lang, _ in settings.LANGUAGES:
            fake = self._get_faker(locale_to_faker[lang])
            data[lang] = fake.format(self.provider, **kwargs)

        return LazyI18nString(data)
