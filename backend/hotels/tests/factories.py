import factory
import factory.fuzzy
from conferences.tests.factories import ConferenceFactory
from factory.django import DjangoModelFactory
from hotels.models import HotelRoom
from i18n.helpers.tests import LanguageFactory
from pytest_factoryboy import register


@register
class HotelRoomFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)

    name = LanguageFactory("name")
    description = LanguageFactory("text")

    total_capacity = factory.Faker("pyint", min_value=10)
    price = factory.Faker("pydecimal", min_value=1, left_digits=4, right_digits=2)

    class Meta:
        model = HotelRoom
