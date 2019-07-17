"""
Stripe implementation of the payment provider.
Allows the website to accept payment using Stripe.
"""
import stripe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from stripe.error import AuthenticationError, CardError, RateLimitError

from ...errors import PaymentError
from ..provider import PaymentProvider
from ..response import PaymentResponse
from ..utils import to_cents


class Stripe(PaymentProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setup(cls):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def charge(self, *, order, payload):
        try:
            intent = stripe.PaymentIntent.create(
                amount=to_cents(order.amount),
                currency="eur",  # TODO: make currency dynamic?
            )
        except CardError as e:
            body = e.json_body
            err = body.get("error", {})

            raise PaymentError(message=_(err.get("message")))
        except RateLimitError as e:
            raise PaymentError(message=_("Please try again in a few hours")) from e
        except AuthenticationError as e:
            raise PaymentError(
                message=_("Something went wrong on our side, please try again")
            ) from e

        order.transaction_id = intent.id
        return PaymentResponse(extras={"client_secret": intent.client_secret})
