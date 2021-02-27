from typing import List, Optional

from association.domain.entities import Subscription
from association.domain.entities.stripe_entities import (
    StripeCheckoutSession,
    StripeCheckoutSessionInput,
    StripeCustomer,
)
from association.domain.repositories import AssociationRepository
from association.tests.factories import StripeProvider


class DummyTransaction:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        pass


class FakeAssociationRepository(AssociationRepository):
    committed: bool = False
    rolledback: bool = False

    def __init__(
        self, subscriptions: list[Subscription], customers: List[StripeCustomer]
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
        # customers
        self.CUSTOMERS_BY_EMAIL = {customer.email: customer for customer in customers}
        print(f"self.SUBSCRIPTIONS_BY_USER_ID : {self.SUBSCRIPTIONS_BY_USER_ID}")

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

    async def list_subscriptions_by_user_id(
        self, user_id: str
    ) -> List[Optional[Subscription]]:
        subscriptions = self.SUBSCRIPTIONS_BY_USER_ID.get(user_id, [])
        if subscriptions and not isinstance(subscriptions, list):
            return [subscriptions]
        return subscriptions

    async def get_subscription_by_user_id(self, user_id: str) -> Optional[Subscription]:
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
        # s = await subscription_factory()
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        fake_session_id = fake.checkout_session_id()

        # if not data.customer_id:
        #     customer_payload.update(dict(customer=data.customer_id))
        # elif data.customer_email:
        #     customer_payload.update(dict(customer_email=data.customer_email))
        # if data.subscription_id:
        #     # TODO TEST ME
        #     customer_payload.update(dict(subscription=data.subscription_id))

        return StripeCheckoutSession(
            id=fake_session_id,
            customer_id=data.customer_id or "",
            subscription_id=data.subscription_id or "",
        )

    # READ FROM STRIPE
    async def retrieve_customer_by_email(self, email: str) -> Optional[StripeCustomer]:
        return self.CUSTOMERS_BY_EMAIL.get(email, None)
