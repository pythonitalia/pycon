import logging
from typing import List, Optional

import stripe
from association.domain.entities.stripe_entities import (
    StripeCheckoutSession,
    StripeCheckoutSessionInput,
    StripeCustomer,
)
from association.domain.entities.subscription_entities import Subscription
from association.domain.exceptions import StripeCheckoutSessionNotCreated
from association.domain.repositories.base import AbstractRepository
from association.settings import (
    STRIPE_SUBSCRIPTION_CANCEL_URL,
    STRIPE_SUBSCRIPTION_PRICE_ID,
    STRIPE_SUBSCRIPTION_SUCCESS_URL,
)
from sqlalchemy import select

logger = logging.getLogger(__name__)


class AssociationRepository(AbstractRepository):

    # READ
    async def get_subscription_by_stripe_id(
        self, stripe_id: str
    ) -> Optional[Subscription]:
        query = select(Subscription).where(Subscription.stripe_id == stripe_id)
        subscription = (await self.session.execute(query)).scalar_one_or_none()
        return subscription

    async def get_subscription_by_session_id(
        self, session_id: str
    ) -> Optional[Subscription]:
        query = select(Subscription).where(Subscription.stripe_session_id == session_id)
        subscription = (await self.session.execute(query)).scalar_one_or_none()
        return subscription

    async def get_subscription_by_customer_id(
        self, customer_id: str
    ) -> Optional[Subscription]:
        query = select(Subscription).where(
            Subscription.stripe_customer_id == customer_id
        )
        subscription = (await self.session.execute(query)).scalar_one_or_none()
        return subscription

    async def list_subscriptions_by_user_id(
        self, user_id: str
    ) -> List[Optional[Subscription]]:
        query = select(Subscription).where(Subscription.user_id == user_id)
        subscriptions = (await self.session.execute(query)).scalars().all()
        return subscriptions

    async def get_subscription_by_user_id(self, user_id: str) -> Optional[Subscription]:
        query = select(Subscription).where(Subscription.user_id == user_id)
        subscription = (await self.session.execute(query)).scalar_one_or_none()
        return subscription

    # WRITE
    async def save_subscription(self, subscription: Subscription) -> Subscription:
        self.session.add(subscription)
        await self.session.flush()
        return subscription

    # ============== #
    #    Stripe
    # ============== #
    # WRITE TO STRIPE
    async def create_checkout_session(
        self, data: StripeCheckoutSessionInput
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
            if data.subscription_id:
                # TODO TEST ME
                customer_payload.update(dict(subscription=data.subscription_id))
            checkout_session_stripe_key = "{CHECKOUT_SESSION_ID}"
            checkout_session = stripe.checkout.Session.create(
                success_url=f"{STRIPE_SUBSCRIPTION_SUCCESS_URL}?session_id={checkout_session_stripe_key}",
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
                id=checkout_session["id"],
                customer_id=checkout_session["customer"] or "",
                subscription_id=checkout_session["subscription"] or "",
            )
        except Exception as e:
            logger.exception("Failure calling stripe.checkout.Session.create service")
            raise StripeCheckoutSessionNotCreated(str(e))

    # READ FROM STRIPE
    async def retrieve_customer_by_email(self, email: str) -> Optional[StripeCustomer]:
        customers = stripe.Customer.list(email=email)
        if len(customers):
            return StripeCustomer(id=customers.data[0].id, email=email)
        return None
