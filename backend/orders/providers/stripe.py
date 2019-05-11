"""
Stripe implementation of the payment provider.
Allows the website to accept payment using Stripe.
"""
import stripe

from django.conf import settings

from .provider import PaymentProvider
from .utils import to_cents


class Stripe(PaymentProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_intent(self, *, payment_method_id, amount):
        return stripe.PaymentIntent.create(
            payment_method=payment_method_id,
            amount=to_cents(amount),
            currency='eur', # TODO: Make dynamic based on the conference?
            confirmation_method='manual',
            confirm=False,
        )

    def charge(self, *, order, token):
        intent = stripe.PaymentIntent.retrieve(token)

        if intent.amount != to_cents(order.amount):
            # TODO: Better exception
            raise ValueError('This payment intent amount is different from the amount of this order')

        confirmed_intent = stripe.PaymentIntent.confirm(token)

        import pdb; pdb.set_trace()
        if confirmed_intent.status == 'requires_action' and confirmed_intent.next_action.type == 'use_stripe_sdk':
            pass
        elif confirmed_intent.status == 'succeeded':
            pass
        else:
            # something went wrong
            pass

        #
        #   if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
        #     # Tell the client to handle the action
        #     return json.dumps({
        #     'requires_action': True,
        #     'payment_intent_client_secret': intent.client_secret,
        #     }), 200
        # elif intent.status == 'succeeded':
        #     # The payment didn’t need any additional actions and completed!
        #     # Handle post-payment fulfillment
        #     return json.dumps({'success': True}), 200
        # else:
        #     # Invalid status
        #     return json.dumps({'error': 'Invalid PaymentIntent status'}), 500

        pass
