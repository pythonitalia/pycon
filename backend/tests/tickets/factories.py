import factory

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from tickets.models import Ticket
from tests.conferences.factories import ConferenceFactory


@register
class TicketFactory(DjangoModelFactory):
    class Meta:
        model = Ticket

    conference = factory.SubFactory(ConferenceFactory)

    name = factory.Faker('name')
    description = factory.Faker('paragraphs')
    price = factory.Faker('random_int', min=20, max=300)
    code = factory.Faker('military_ship')

    start = factory.Faker('past_date')
    end = factory.Faker('future_date')
