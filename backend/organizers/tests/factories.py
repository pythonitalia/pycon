import factory
import factory.fuzzy
from organizers.models import Organizer
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


@register
class OrganizerFactory(DjangoModelFactory):
    class Meta:
        model = Organizer

    name = factory.Faker("word")
    slug = factory.Faker("slug")
