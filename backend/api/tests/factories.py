import string

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from ..models import APIToken


@register
class TokenFactory(DjangoModelFactory):
    token = factory.fuzzy.FuzzyText(length=100, chars=string.ascii_letters)

    class Meta:
        model = APIToken
