import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from checklist.models import ChecklistItem


@register
class ChecklistItemFactory(DjangoModelFactory):
    text = factory.Faker("text")

    class Meta:
        model = ChecklistItem
