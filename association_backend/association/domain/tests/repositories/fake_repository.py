from collections import defaultdict
from typing import List, Optional

from association.domain.entities import Subscription, SubscriptionPayment
from association.domain.entities.stripe import (
    StripeCheckoutSession,
    StripeCheckoutSessionInput,
    StripeCustomer,
    StripeSubscription,
)
from association.domain.exceptions import MultipleCustomerReturned
from association.domain.repositories import AssociationRepository
from association.tests.factories import SubscriptionFactory


class DummyTransaction:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        pass


class FakeAssociationRepository(AssociationRepository):
    committed: bool = False
    rolledback: bool = False

    def __init__(
        self,
        subscriptions: List[Subscription],
        customers: List[StripeCustomer],
        subscription_payments: Optional[List[SubscriptionPayment]] = None,
        checkout_sessions: Optional[List[StripeCheckoutSession]] = None,
        stripe_subscriptions: Optional[List[StripeSubscription]] = None,
    ) -> None:
        super().__init__()
        # subscriptions
        self.SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID = {
            subscription.stripe_subscription_id: subscription
            for subscription in subscriptions
        }
        self.SUBSCRIPTIONS_BY_SESSION_ID = {
            subscription.stripe_session_id: subscription
            for subscription in subscriptions
        }
        self.SUBSCRIPTIONS_BY_CUSTOMER_ID = {
            subscription.stripe_customer_id: subscription
            for subscription in subscriptions
        }
        self.SUBSCRIPTIONS_BY_USER_ID = {
            subscription.user_id: subscription for subscription in subscriptions
        }
        # checkout-sessions
        if checkout_sessions:
            self.CHECKOUT_SESSIONS_BY_ID = {
                checkout_session.id: checkout_session
                for checkout_session in checkout_sessions
            }
        # payments
        self.SUBSCRIPTION_PAYMENTS_BY_STRIPE_ID = {}
        if subscription_payments:
            self.SUBSCRIPTION_PAYMENTS_BY_STRIPE_ID = {
                subscription_payment.subscription.stripe_subscription_id: subscription_payment
                for subscription_payment in subscription_payments
            }
        # customers
        self.CUSTOMERS_BY_EMAIL = defaultdict(list)
        [
            self.CUSTOMERS_BY_EMAIL[customer.email].append(customer)
            for customer in customers
        ]
        # stripe subscriptions
        self.STRIPE_SUBSCRIPTIONS_BY_ID = {}
        if stripe_subscriptions:
            self.STRIPE_SUBSCRIPTIONS_BY_ID = {
                stripe_subscription.id: stripe_subscription
                for stripe_subscription in stripe_subscriptions
            }

    def transaction(self):
        return DummyTransaction()

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolledback = True

    # READ
    async def get_subscription_by_stripe_subscription_id(
        self, stripe_subscription_id: str
    ) -> Optional[Subscription]:
        return self.SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID.get(
            stripe_subscription_id, None
        )

    async def get_subscription_by_session_id(
        self, session_id: str
    ) -> Optional[Subscription]:
        return self.SUBSCRIPTIONS_BY_SESSION_ID.get(session_id, None)

    async def get_subscription_by_customer_id(
        self, customer_id: str
    ) -> Optional[Subscription]:
        return self.SUBSCRIPTIONS_BY_CUSTOMER_ID.get(customer_id, None)

    async def get_subscription_by_user_id(self, user_id: int) -> Optional[Subscription]:
        return self.SUBSCRIPTIONS_BY_USER_ID.get(user_id, None)

    # WRITE
    async def save_subscription(self, subscription: Subscription) -> Subscription:
        new_subscription = subscription
        self.SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID[
            new_subscription.stripe_subscription_id
        ] = new_subscription
        self.SUBSCRIPTIONS_BY_SESSION_ID[
            new_subscription.stripe_session_id
        ] = new_subscription
        self.SUBSCRIPTIONS_BY_CUSTOMER_ID[
            new_subscription.stripe_customer_id
        ] = new_subscription
        self.SUBSCRIPTIONS_BY_USER_ID[new_subscription.user_id] = new_subscription
        return new_subscription

    # WRITE
    async def delete_subscription(self, subscription: Subscription) -> None:
        self.SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID.pop(
            subscription.stripe_subscription_id
        )
        self.SUBSCRIPTIONS_BY_SESSION_ID.pop(subscription.stripe_session_id)
        self.SUBSCRIPTIONS_BY_CUSTOMER_ID.pop(subscription.stripe_customer_id)
        self.SUBSCRIPTIONS_BY_USER_ID.pop(subscription.user_id)
        return None

    # WRITE
    async def save_payment(
        self, subscription_payment: SubscriptionPayment
    ) -> SubscriptionPayment:
        self.SUBSCRIPTION_PAYMENTS_BY_STRIPE_ID[
            subscription_payment.subscription.stripe_subscription_id
        ] = subscription_payment
        return subscription_payment

    # ============== #
    #    Stripe
    # ============== #
    # WRITE TO STRIPE
    async def create_checkout_session(
        self, data: StripeCheckoutSessionInput
    ) -> Optional[StripeCheckoutSession]:
        fake_session_id = SubscriptionFactory.build().stripe_session_id
        return StripeCheckoutSession(
            id=fake_session_id, customer_id=data.customer_id or ""
        )

    async def retrieve_customer_portal_session_url(self, stripe_customer_id):
        return f"https://stripe.com/stripe_test_customer_portal/{stripe_customer_id}"

    # READ FROM STRIPE
    async def retrieve_customer_by_email(self, email: str) -> Optional[StripeCustomer]:
        customers = self.CUSTOMERS_BY_EMAIL.get(email, [])
        if len(customers) > 1:
            raise MultipleCustomerReturned()
        elif len(customers) > 0:
            return customers[0]
        return None

    async def retrieve_stripe_checkout_session(
        self, stripe_session_id: str
    ) -> Optional[StripeCheckoutSession]:
        print(f"{self.CHECKOUT_SESSIONS_BY_ID = }")
        return self.CHECKOUT_SESSIONS_BY_ID.get(stripe_session_id, None)

    async def retrieve_stripe_subscription(
        self, stripe_subscription_id: str
    ) -> Optional[StripeSubscription]:
        print(f"{self.STRIPE_SUBSCRIPTIONS_BY_ID = }")
        return self.STRIPE_SUBSCRIPTIONS_BY_ID.get(stripe_subscription_id, None)

    async def retrieve_external_subscription_by_session_id(
        self, stripe_session_id: str
    ) -> Optional[StripeSubscription]:
        checkout_session = await self.retrieve_stripe_checkout_session(
            stripe_session_id
        )
        if checkout_session.subscription_id:
            subscription = await self.retrieve_stripe_subscription(
                checkout_session.subscription_id
            )
            return subscription
        return None
