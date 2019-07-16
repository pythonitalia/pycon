import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from voting.models import VoteRange


@register
class VoteRangeFactory(DjangoModelFactory):
    class Meta:
        model = VoteRange
        django_get_or_create = ("name",)

    name = factory.Faker("word")
    first = 1  # factory.Faker('pyint')
    last = 10  # factory.Faker('pyint')
    step = 0.5  # factory.Faker('pyfloat', min_value=first, max_value=last)
