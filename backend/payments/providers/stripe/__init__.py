"""
Stripe implementation of the payment provider.
Allows the website to accept payment using Stripe.
"""
import stripe

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from stripe.error import CardError, RateLimitError, AuthenticationError

from .errors import Stripe3DVerificationError

from ...exceptions import PaymentFailedError
from ..provider import PaymentProvider
from ..utils import to_cents


class Stripe(PaymentProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def charge(self, *, order, payload):
        payment_method_id = payload.get('payment_method_id', None)
        payment_intent_id = payload.get('payment_intent_id', None)

        if payment_intent_id and payment_method_id:
            raise ValueError(_('You cannot specify both payment_method_id and payment_intent_id'))

        try:
            if payment_method_id:
                intent = stripe.PaymentIntent.create(
                    payment_method=payment_method_id,
                    amount=to_cents(order.amount),
                    currency='eur', # TODO: make currency dynamic?
                    confirmation_method='manual',
                    confirm=True
                )
            elif payment_intent_id:
                intent = stripe.PaymentIntent.confirm(payment_intent_id)
            else:
                raise ValueError(_("You need to specify at least a payment_method_id or a payment_intent_id"))
        except CardError as e:
            body = e.json_body
            err  = body.get('error', {})

            raise PaymentFailedError(message=_(err.get('message')))
        except RateLimitError as e:
            raise PaymentFailedError(message=_('Please try again in a few hours'))
        except AuthenticationError as e:
            raise PaymentFailedError(message=_('Something went wrong on our side, please try again'))

        if intent.amount != to_cents(order.amount):
            # TODO: Better exception
            raise ValueError(_('Payment intent amount and cart amount different'))

        if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
            raise Stripe3DVerificationError(intent.client_secret)
        elif intent.status == 'succeeded':
            order.transaction_id = intent.id
            return True
        else:
            # something went wrong
            raise PaymentFailedError()
