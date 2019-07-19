import strawberry
from strawberry_forms.mutations import FormMutation

from .forms import BuyTicketWithStripeForm
from .types import GenericPaymentError, StripeClientSecret


class BuyTicketWithStripe(FormMutation):
    class Meta:
        form_class = BuyTicketWithStripeForm
        output_types = (GenericPaymentError, StripeClientSecret)


@strawberry.type
class PaymentsMutations:
    buy_ticket_with_stripe = BuyTicketWithStripe.Mutation
