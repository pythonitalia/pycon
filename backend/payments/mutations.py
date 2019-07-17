from graphene import ObjectType
from graphene_form.mutations import FormMutation

from .forms import BuyTicketWithStripeForm
from .types import GenericPaymentError, StripeClientSecret


class BuyTicketWithStripe(FormMutation):
    class Meta:
        form_class = BuyTicketWithStripeForm
        output_types = (GenericPaymentError, StripeClientSecret)


class PaymentsMutations(ObjectType):
    buy_ticket_with_stripe = BuyTicketWithStripe.Field()
