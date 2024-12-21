import factory
import factory.fuzzy
from organizers.models import Organizer
from factory.django import DjangoModelFactory


class OrganizerFactory(DjangoModelFactory):
    class Meta:
        model = Organizer

    name = factory.Faker("word")
    slug = factory.Faker("word")
