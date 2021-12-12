import logging
from typing import Optional

import ormar
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
    async def get_user_subscription(
        self, user: PastaportoUserInfo
    ) -> Optional[Subscription]:
        subscription = await Subscription.objects.get_or_none(user_id=user.id)
        return subscription

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

    # async def get_customer_for_user_id(self, user_id: UserID) -> Optional[StripeCustomer]:
    #     customer = await StripeCustomer.objects.get_or_none(
    #         user_id=stripe_customer_id
    #     )
    #     return customer

    # async def get_by_stripe_id(
    #     self, stripe_subscription_id: str
    # ) -> Optional[Subscription]:
    #     return await Subscription.objects.get_or_none(
    #         stripe_subscription_id=stripe_subscription_id
    #     )

    # async def get_or_create_subscription(
    #     self,
    #     *,
    #     customer: Customer,
    #     stripe_subscription_id: str,
    # ) -> Subscription:
    #     try:
    #         subscription = await Subscription.objects.get(
    #             stripe_subscription_id=stripe_subscription_id
    #         )

    #         if subscription.customer.id != customer.id:
    #             logger.error(
    #                 "Trying to get stripe_subscription_id=%s for customer_id=%s"
    #                 " but the customer associated to the"
    #                 " found subscription (associated_customer_id=%s)"
    #                 " is not the same as passed customer",
    #                 stripe_subscription_id,
    #                 customer.id,
    #                 subscription.customer.id,
    #             )
    #             raise ValueError("Subscription found but assigned to another customer")
    #     except ormar.NoMatch:
    #         subscription = await Subscription.objects.create(
    #             stripe_subscription_id=stripe_subscription_id,
    #             customer=customer,
    #             status=SubscriptionStatus.PENDING,
    #         )

    #     return subscription

    # async def save_subscription(self, subscription: Subscription) -> Subscription:
    #     await subscription.update()

    #     for invoice in subscription._add_invoice:
    #         invoice.subscription = subscription
    #         await invoice.save()
    #         await subscription.invoices.add(invoice)

    #     return subscription
