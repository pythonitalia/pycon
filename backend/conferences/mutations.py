import graphene

from api.mutations import AuthOnlyDjangoFormMutation

from .forms import BuyTicketForm


class BuyTicket(AuthOnlyDjangoFormMutation):
    class Meta:
        form_class = BuyTicketForm
        exclude_output_fields = ('payload', 'items')

class ConferencesMutations(graphene.ObjectType):
    buy_ticket = BuyTicket.Field()
