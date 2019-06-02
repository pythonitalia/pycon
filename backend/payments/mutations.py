from graphene import ObjectType

from graphene_form.mutations import FormMutation

from .forms import BuyTicketWithStripeForm

from .providers.stripe.types import Stripe3DValidationRequired
from .types import GenericPaymentFailedError


class BuyTicketWithStripe(FormMutation):
    class Meta:
        form_class = BuyTicketWithStripeForm
        output_types = (Stripe3DValidationRequired, GenericPaymentFailedError,)


class PaymentsMutations(ObjectType):
    buy_ticket_with_stripe = BuyTicketWithStripe.Field()
