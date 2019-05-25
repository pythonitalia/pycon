from graphene import ObjectType

from graphene_form.mutations import FormMutation

from .forms import BuyTicketWithStripeForm

from .types import Stripe3DValidationRequired


class BuyTicketWithStripe(FormMutation):
    class Meta:
        form_class = BuyTicketWithStripeForm
        output_types = (Stripe3DValidationRequired, )


class PaymentsMutations(ObjectType):
    buy_ticket_with_stripe = BuyTicketWithStripe.Field()
