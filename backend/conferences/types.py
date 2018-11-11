import graphene

from graphene_django import DjangoObjectType

from tickets.types import TicketType

from .models import Conference, Deadline


class DeadlineModelType(DjangoObjectType):
    class Meta:
        model = Deadline
        only_fields = (
            'conference',
            'type',
            'name',
            'start',
            'end',
        )


class ConferenceType(DjangoObjectType):
    tickets = graphene.NonNull(graphene.List(graphene.NonNull(TicketType)))
    deadlines = graphene.NonNull(graphene.List(graphene.NonNull(DeadlineModelType)))

    def resolve_tickets(self, info):
        return self.tickets.all()

    def resolve_deadlines(self, info):
        return self.deadlines.order_by('start').all()

    class Meta:
        model = Conference
        only_fields = (
            'id',
            'name',
            'code',
            'start',
            'end',
            'deadlines'
        )
