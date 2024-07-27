import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from checklist.models import ChecklistItem


class ChecklistItemFactory(DjangoModelFactory):
    text = factory.Faker("text")

    class Meta:
        model = ChecklistItem
