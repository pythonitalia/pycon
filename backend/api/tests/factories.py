import string

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from ..models import APIToken


class TokenFactory(DjangoModelFactory):
    token = factory.fuzzy.FuzzyText(length=100, chars=string.ascii_letters)

    class Meta:
        model = APIToken
