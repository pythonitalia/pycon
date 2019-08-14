from countries.models import Country
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


@register
class CountriesFactory(DjangoModelFactory):
    class Meta:
        model = Country
        django_get_or_create = ("code",)
