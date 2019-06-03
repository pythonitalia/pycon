"""
Stripe implementation of the payment provider.
Allows the website to accept payment using Stripe.
"""
import stripe

from django.conf import settings

from orders.enums import PaymentState

from .exceptions import Stripe3DVerificationException

from ...exceptions import PaymentFailed
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
            # TODO: Change Exception or error handling
            raise ValueError('Cannot specify both')

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
            # TODO: Better exception
            raise ValueError('Specify at least method or intent id')

        if intent.amount != to_cents(order.amount):
            # TODO: Better exception
            raise ValueError('This payment intent amount is different from the amount of this order')

        # import pdb; pdb.set_trace()
        if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
            raise Stripe3DVerificationException(intent.client_secret)
        elif intent.status == 'succeeded':
            order.transaction_id = intent.id
            return PaymentState.COMPLETED
        else:
            # something went wrong
            raise PaymentFailed()
