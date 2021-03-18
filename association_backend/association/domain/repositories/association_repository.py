import logging
from typing import Optional

import stripe
from sqlalchemy import select

from association.domain.entities.stripe import (
    StripeCheckoutSession,
    StripeCheckoutSessionInput,
    StripeCustomer,
)
from association.domain.entities.subscriptions import Subscription, SubscriptionPayment
from association.domain.exceptions import MultipleCustomerReturned
from association.domain.repositories.base import AbstractRepository
from association.settings import (
    DOMAIN_URL,
    STRIPE_SUBSCRIPTION_API_SECRET,
    STRIPE_SUBSCRIPTION_CANCEL_URL,
    STRIPE_SUBSCRIPTION_PRICE_ID,
    STRIPE_SUBSCRIPTION_SUCCESS_URL,
)

logger = logging.getLogger(__name__)


class AssociationRepository(AbstractRepository):

    # READ
    async def get_subscription_by_stripe_subscription_id(
        self, stripe_subscription_id: str
    ) -> Optional[Subscription]:
        query = select(Subscription).where(
            Subscription.stripe_subscription_id == stripe_subscription_id
        )
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

    async def get_subscription_by_user_id(self, user_id: int) -> Optional[Subscription]:
        query = select(Subscription).where(Subscription.user_id == user_id)
        subscription = (await self.session.execute(query)).scalar_one_or_none()
        return subscription

    # WRITE
    async def save_subscription(self, subscription: Subscription) -> Subscription:
        """ TODO Test Create or Update """
        self.session.add(subscription)
        await self.session.flush()
        return subscription

    async def save_payment(
        self, subscription_payment: SubscriptionPayment
    ) -> SubscriptionPayment:
        """ TODO Test ME """
        self.session.add(subscription_payment)
        await self.session.flush()
        return subscription_payment

    # ============== #
    #    Stripe
    # ============== #
    # WRITE TO STRIPE
    async def create_checkout_session(
        self, data: StripeCheckoutSessionInput
    ) -> StripeCheckoutSession:
        """ TODO Test ME """
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
        checkout_session_stripe_key = "{CHECKOUT_SESSION_ID}"
        checkout_session = stripe.checkout.Session.create(
            success_url=f"{STRIPE_SUBSCRIPTION_SUCCESS_URL}?session_id={checkout_session_stripe_key}",
            cancel_url=STRIPE_SUBSCRIPTION_CANCEL_URL,
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": STRIPE_SUBSCRIPTION_PRICE_ID,
                    "quantity": 1,
                }
            ],
            **customer_payload,
            api_key=STRIPE_SUBSCRIPTION_API_SECRET,
        )
        logger.info(f"checkout_session: {checkout_session}")
        return StripeCheckoutSession(
            id=checkout_session["id"],
            customer_id=checkout_session["customer"] or "",
            subscription_id=checkout_session["subscription"] or "",
        )

    async def retrieve_customer_portal_session_url(self, customer_id: str) -> str:
        """ TODO Test ME """
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=DOMAIN_URL,
            api_key=STRIPE_SUBSCRIPTION_API_SECRET,
        )
        return session.url

    # READ FROM STRIPE
    async def retrieve_customer_by_email(self, email: str) -> Optional[StripeCustomer]:
        """ TODO Test ME """
        customers = stripe.Customer.list(
            email=email, api_key=STRIPE_SUBSCRIPTION_API_SECRET
        )
        if len(customers) > 1:
            raise MultipleCustomerReturned()
        elif len(customers) > 0:
            return StripeCustomer(id=customers.data[0].id, email=email)
        return None

    async def retrieve_checkout_session_by_id(
        self, stripe_session_id: str
    ) -> Optional[StripeCheckoutSession]:
        """ TODO Test ME """
        checkout_session = stripe.checkout.Session.retrieve(
            stripe_session_id, api_key=STRIPE_SUBSCRIPTION_API_SECRET
        )
        logger.info(f"checkout_session: {checkout_session}")
        return StripeCheckoutSession(
            id=checkout_session["id"],
            customer_id=checkout_session["customer"] or "",
            subscription_id=checkout_session["subscription"] or "",
        )
