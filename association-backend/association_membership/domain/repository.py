import logging
from typing import Optional

import ormar
import stripe

from association.domain.entities.stripe import StripeCheckoutSession
from association.settings import STRIPE_SUBSCRIPTION_PRICE_ID
from association_membership.domain.entities import Subscription, SubscriptionStatus
from customers.domain.entities import Customer

logger = logging.getLogger(__name__)


class AssociationMembershipRepository:
    async def get_by_stripe_id(
        self, stripe_subscription_id: str
    ) -> Optional[Subscription]:
        return await Subscription.objects.get_or_none(
            stripe_subscription_id=stripe_subscription_id
        )

    async def get_or_create_subscription(
        self,
        *,
        customer: Customer,
        stripe_subscription_id: str,
    ) -> Subscription:
        try:
            subscription = await Subscription.objects.get(
                stripe_subscription_id=stripe_subscription_id
            )

            if subscription.customer.id != customer.id:
                raise ValueError(
                    "Subscription X found but assigned to another customer"
                )
        except ormar.NoMatch:
            subscription = await Subscription.objects.create(
                stripe_subscription_id=stripe_subscription_id,
                customer=customer,
                status=SubscriptionStatus.PENDING,
            )

        return subscription

    async def save_subscription(self, subscription: Subscription) -> Subscription:
        """ TODO Test Create or Update """
        await subscription.update()

        for invoice in subscription._add_invoice:
            # invoices to add
            invoice.subscription = subscription
            await invoice.save()

            await subscription.subscriptioninvoices.add(invoice)

        return subscription

    async def create_checkout_session(self, customer_id: str) -> StripeCheckoutSession:
        checkout_session = stripe.checkout.Session.create(
            success_url="https://example.org",
            cancel_url="https://example.org",
            payment_method_types=["card"],
            mode="subscription",
            customer=customer_id,
            line_items=[
                {
                    "price": STRIPE_SUBSCRIPTION_PRICE_ID,
                    "quantity": 1,
                }
            ],
        )
        return StripeCheckoutSession(
            id=checkout_session["id"],
        )
