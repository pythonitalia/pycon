import logging
from typing import Optional

import stripe
from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo

from src.association.settings import (
    ASSOCIATION_FRONTEND_URL,
    STRIPE_SUBSCRIPTION_PRICE_ID,
)
from src.association_membership.domain.entities import (
    StripeCustomer,
    Subscription,
    SubscriptionStatus,
)

logger = logging.getLogger(__name__)


class AssociationMembershipRepository:
    async def get_user_subscription(self, user_id: int) -> Optional[Subscription]:
        subscription = await Subscription.objects.get_or_none(user_id=user_id)
        return subscription

    async def get_stripe_customer_from_user_id(
        self, user_id: int
    ) -> Optional[StripeCustomer]:
        return await StripeCustomer.objects.get_or_none(user_id=user_id)

    async def create_subscription(self, user: PastaportoUserInfo) -> Subscription:
        subscription = await Subscription.objects.create(
            user_id=user.id, status=SubscriptionStatus.PENDING
        )

        # TODO check existing customer and re-use it?
        stripe_customer = stripe.Customer.create(
            email=user.email, metadata={"user_id": user.id}
        )

        await StripeCustomer.objects.create(
            user_id=user.id, stripe_customer_id=stripe_customer.id
        )
        return subscription

    async def get_subscription_from_stripe_customer(
        self, stripe_customer_id: str
    ) -> Optional[Subscription]:
        stripe_customer = await StripeCustomer.objects.get_or_none(
            stripe_customer_id=stripe_customer_id
        )

        if not stripe_customer:
            return None

        subscription = await Subscription.objects.get_or_none(
            user_id=stripe_customer.user_id
        )
        return subscription

    async def create_checkout_session(self, subscription: Subscription) -> str:
        customer = await StripeCustomer.objects.get(
            user_id=subscription.user_id,
        )

        checkout_session = stripe.checkout.Session.create(
            success_url=f"{ASSOCIATION_FRONTEND_URL}?membership-status=success#membership",
            cancel_url=f"{ASSOCIATION_FRONTEND_URL}#membership",
            payment_method_types=["card"],
            mode="subscription",
            customer=customer.stripe_customer_id,
            # Note: if adding more line items, make sure webhook handlers
            # can handle it when fetching the period start/end dates
            line_items=[
                {
                    "price": STRIPE_SUBSCRIPTION_PRICE_ID,
                    "quantity": 1,
                }
            ],
        )
        return checkout_session.id

    async def create_stripe_portal_session_url(
        self, stripe_customer: StripeCustomer
    ) -> str:
        session = stripe.billing_portal.Session.create(
            customer=stripe_customer.stripe_customer_id
        )
        return session.url

    async def save_subscription(self, subscription: Subscription) -> Subscription:
        await subscription.update()

        for (
            stripe_subscription_payment
        ) in subscription._add_stripe_subscription_payment:
            await stripe_subscription_payment.payment.save()
            await stripe_subscription_payment.save()

        return subscription
