from users.tests.factories import UserFactory
import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from conferences.tests.factories import ConferenceFactory
from hotels.models import BedLayout, HotelRoom, HotelRoomReservation
from i18n.tests.factories import LanguageFactory


class HotelRoomFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)

    name = LanguageFactory("name")
    description = LanguageFactory("text")

    total_capacity = factory.Faker("pyint", min_value=10)
    price = factory.Faker("pydecimal", min_value=1, left_digits=4, right_digits=2)

    class Meta:
        model = HotelRoom


class HotelRoomReservationFactory(DjangoModelFactory):
    order_code = "AAAABB"
    room = factory.SubFactory(HotelRoomFactory)
    checkin = factory.Faker("past_date")
    checkout = factory.Faker("future_date")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = HotelRoomReservation


class BedLayoutFactory(DjangoModelFactory):
    name = LanguageFactory("name")

    class Meta:
        model = BedLayout
