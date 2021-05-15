import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from hotels.models import HotelRoom, HotelRoomReservation
from i18n.tests.factories import LanguageFactory


@register
class HotelRoomFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)

    name = LanguageFactory("name")
    description = LanguageFactory("text")

    total_capacity = factory.Faker("pyint", min_value=10)
    price = factory.Faker("pydecimal", min_value=1, left_digits=4, right_digits=2)

    class Meta:
        model = HotelRoom


@register
class HotelRoomReservationFactory(DjangoModelFactory):
    order_code = "AAAABB"
    room = factory.SubFactory(HotelRoomFactory)
    user_id = factory.Faker("pyint", min_value=1)
    checkin = factory.Faker("past_date")
    checkout = factory.Faker("future_date")

    class Meta:
        model = HotelRoomReservation
