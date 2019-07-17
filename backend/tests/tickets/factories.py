import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from tests.conferences.factories import TicketFareFactory
from tests.orders.factories import OrderFactory
from tests.users.factories import UserFactory
from tickets.models import Ticket


@register
class TicketFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ticket_fare = factory.SubFactory(TicketFareFactory)
    order = factory.SubFactory(OrderFactory)

    class Meta:
        model = Ticket
