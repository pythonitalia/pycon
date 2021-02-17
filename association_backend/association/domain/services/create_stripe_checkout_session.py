import logging
from typing import Optional

import stripe
from association.domain.entities.stripe_entities import StripeCheckoutSession
from association.domain.services.exceptions import StripeCheckoutSessionNotCreated
from association.settings import (
    STRIPE_SUBSCRIPTION_API_SECRET,
    STRIPE_SUBSCRIPTION_CANCEL_URL,
    STRIPE_SUBSCRIPTION_PRICE_ID,
    STRIPE_SUBSCRIPTION_SUCCESS_URL,
)
from pydantic import BaseModel

logger = logging.getLogger(__name__)

stripe.api_key = STRIPE_SUBSCRIPTION_API_SECRET  # 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


class StripeCreateCheckoutInput(BaseModel):
    customer_email: Optional[str]
    customer_id: Optional[str]


async def create_checkout_session(
    data: StripeCreateCheckoutInput
) -> Optional[StripeCheckoutSession]:
    try:
        # See https://stripe.com/docs/api/checkout/sessions/create
        # for additional parameters to pass.
        # {CHECKOUT_SESSION_ID} is a string literal; do not change it!
        # the actual Session ID is returned in the query parameter when your customer
        # is redirected to the success page.
        customer_payload = {}
        if data.customer_id:
            customer_payload.update(dict(customer=data.customer_id))
        elif data.customer_email:
            customer_payload.update(dict(customer_email=data.customer_email))
        checkout_session = stripe.checkout.Session.create(
            success_url=STRIPE_SUBSCRIPTION_SUCCESS_URL
            + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=STRIPE_SUBSCRIPTION_CANCEL_URL,
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": STRIPE_SUBSCRIPTION_PRICE_ID,
                    # For metered billing, do not pass quantity
                    "quantity": 1,
                }
            ],
            **customer_payload,
        )
        logger.info(f"checkout_session: {checkout_session}")
        return StripeCheckoutSession(
            id=checkout_session["id"], customer_id=checkout_session["customer"] or ""
        )
    except Exception as e:
        logger.exception("Failure calling stripe.checkout.Session.create service")
        raise StripeCheckoutSessionNotCreated(str(e))
        # return json.dumps({'error': {'message': str(e)}}), 400
