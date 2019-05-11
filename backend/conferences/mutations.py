import graphene

from api.mutations import AuthOnlyDjangoFormMutation

from .forms import BuyTicketForm, CreateStripeIntentForm


class BuyTicket(AuthOnlyDjangoFormMutation):
    class Meta:
        form_class = BuyTicketForm


class CreateStripeIntent(AuthOnlyDjangoFormMutation):
    payment_intent_id = graphene.NonNull(graphene.String)

    class Meta:
        form_class = CreateStripeIntentForm


class ConferencesMutations(graphene.ObjectType):
    buy_ticket = BuyTicket.Field()
    create_stripe_intent = CreateStripeIntent.Field()
