import graphene

from .models import Conference

from graphene_django import DjangoObjectType

from tickets.types import TicketType


class ConferenceType(DjangoObjectType):
    tickets = graphene.List(graphene.NonNull(TicketType))

    def resolve_tickets(self, info):
        return self.tickets.all()

    class Meta:
        model = Conference
        only_fields = ('id', 'start', 'end', 'name', 'slug')
