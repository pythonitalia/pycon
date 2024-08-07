import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from languages.models import Language


class LanguageFactory(DjangoModelFactory):
    class Meta:
        model = Language
        django_get_or_create = ("code",)

    code = factory.fuzzy.FuzzyChoice(("it", "en"))
