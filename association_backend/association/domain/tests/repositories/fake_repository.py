from typing import List, Optional

from association.domain.entities import Subscription
from association.domain.entities.stripe_entities import (
    StripeCheckoutSession,
    StripeCheckoutSessionInput,
    StripeCustomer,
)
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
        checkout_sessions: Optional[List[StripeCheckoutSession]] = None,
    ) -> None:
        super().__init__()
        # subscriptions
        self.SUBSCRIPTIONS_BY_STRIPE_ID = {
            subscription.stripe_id: subscription for subscription in subscriptions
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
        # customers
        self.CUSTOMERS_BY_EMAIL = {customer.email: customer for customer in customers}

    def transaction(self):
        return DummyTransaction()

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolledback = True

    # READ
    async def get_subscription_by_stripe_id(
        self, stripe_id: str
    ) -> Optional[Subscription]:
        return self.SUBSCRIPTIONS_BY_STRIPE_ID.get(stripe_id, None)

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
        self.SUBSCRIPTIONS_BY_STRIPE_ID[new_subscription.stripe_id] = new_subscription
        self.SUBSCRIPTIONS_BY_SESSION_ID[
            new_subscription.stripe_session_id
        ] = new_subscription
        self.SUBSCRIPTIONS_BY_CUSTOMER_ID[
            new_subscription.stripe_customer_id
        ] = new_subscription
        self.SUBSCRIPTIONS_BY_USER_ID[new_subscription.user_id] = new_subscription
        return new_subscription

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
        return self.CUSTOMERS_BY_EMAIL.get(email, None)

    async def retrieve_checkout_session_by_id(
        self, stripe_id: str
    ) -> Optional[StripeCheckoutSession]:
        return self.CHECKOUT_SESSIONS_BY_ID.get(stripe_id, None)
