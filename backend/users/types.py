from graphene import ID, List, NonNull
from graphene_django import DjangoObjectType
from tickets.types import TicketType

from .models import User


class MeUserType(DjangoObjectType):
    tickets = NonNull(List(NonNull(TicketType)), conference=ID())

    def resolve_tickets(self, info, conference):
        return self.tickets.filter(ticket_fare__conference__code=conference).all()

    class Meta:
        model = User
        only_fields = ("id", "email", "tickets")


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ("id", "email", "name", "username")
