from .models import Ticket

from graphene_django import DjangoObjectType


class TicketType(DjangoObjectType):
    class Meta:
        model = Ticket
        only_fields = ('id', 'code', 'name', 'price', 'start', 'end', 'description')
