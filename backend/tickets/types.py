from graphene_django import DjangoObjectType
from tickets.models import Ticket


class TicketType(DjangoObjectType):
    class Meta:
        model = Ticket
