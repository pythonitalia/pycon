import graphene

from .models import Conference

from graphene_django import DjangoObjectType

from tickets.types import TicketType


class ConferenceType(DjangoObjectType):
    tickets = graphene.NonNull(graphene.List(graphene.NonNull(TicketType)))

    def resolve_tickets(self, info):
        return self.tickets.all()

    class Meta:
        model = Conference
        only_fields = (
            'id',
            'name',
            'code',
            'start',
            'end',
            'cfp_start',
            'cfp_end',
            'voting_start',
            'voting_end',
            'refund_start',
            'refund_end'
        )
