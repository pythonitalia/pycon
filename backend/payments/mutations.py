from graphene import ObjectType, List

from graphene_form.mutations import FormMutation

from .forms import BuyTicketWithStripeForm

from .providers.stripe.types import Stripe3DValidationRequired
from .types import GenericPaymentError, TicketsPayment


class BuyTicketWithStripe(FormMutation):
    class Meta:
        form_class = BuyTicketWithStripeForm
        output_types = (
            Stripe3DValidationRequired,
            GenericPaymentError,
            TicketsPayment
        )


class PaymentsMutations(ObjectType):
    buy_ticket_with_stripe = BuyTicketWithStripe.Field()
