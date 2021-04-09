from collections import defaultdict
from typing import List, Optional

from association.domain.entities import Subscription, SubscriptionPayment
from association.domain.entities.stripe import (
    StripeCheckoutSession,
    StripeCustomer,
    StripeSubscription,
    StripeSubscriptionStatus,
)
from association.domain.exceptions import (
    MultipleCustomerReturned,
    MultipleCustomerSubscriptionsReturned,
    StripeSubscriptionNotFound,
)
from association.domain.repositories import AssociationRepository
from association.tests.factories import (
    StripeCheckoutSessionFactory,
    StripeCustomerFactory,
)


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
        subscriptions: Optional[List[Subscription]] = None,
        subscription_payments: Optional[List[SubscriptionPayment]] = None,
        stripe_checkout_sessions: Optional[List[StripeCheckoutSession]] = None,
        stripe_customers: Optional[List[StripeCustomer]] = None,
        stripe_subscriptions: Optional[List[StripeSubscription]] = None,
    ) -> None:
        super().__init__()

        # subscriptions
        self.SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID = {}
        self.SUBSCRIPTIONS_BY_CUSTOMER_ID = {}
        self.SUBSCRIPTIONS_BY_USER_ID = {}
        if subscriptions:
            self.SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID = {
                subscription.stripe_subscription_id: subscription
                for subscription in subscriptions
            }
            self.SUBSCRIPTIONS_BY_CUSTOMER_ID = {
                subscription.stripe_customer_id: subscription
                for subscription in subscriptions
            }
            self.SUBSCRIPTIONS_BY_USER_ID = {
                subscription.user_id: subscription for subscription in subscriptions
            }

        # payments
        self.SUBSCRIPTION_PAYMENTS_BY_STRIPE_ID = {}
        self.SUBSCRIPTION_PAYMENTS_BY_INVOICE_ID = {}
        if subscription_payments:
            self.SUBSCRIPTION_PAYMENTS_BY_STRIPE_ID = {
                subscription_payment.subscription.stripe_subscription_id: subscription_payment
                for subscription_payment in subscription_payments
            }
            self.SUBSCRIPTION_PAYMENTS_BY_INVOICE_ID = {
                subscription_payment.stripe_invoice_id: subscription_payment
                for subscription_payment in subscription_payments
            }

        # STRIPE
        # checkout-sessions
        self.STRIPE_CHECKOUT_SESSIONS_BY_ID = {}
        if stripe_checkout_sessions:
            self.STRIPE_CHECKOUT_SESSIONS_BY_ID = {
                checkout_session.id: checkout_session
                for checkout_session in stripe_checkout_sessions
            }

        # stripe customers
        self.STRIPE_CUSTOMERS_BY_EMAIL = defaultdict(list)
        if stripe_customers:
            [
                self.STRIPE_CUSTOMERS_BY_EMAIL[customer.email].append(customer)
                for customer in stripe_customers
            ]

        # stripe subscriptions
        self.STRIPE_SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID = {}
        self.STRIPE_SUBSCRIPTIONS_BY_STRIPE_CUSTOMER_ID = defaultdict(list)
        if stripe_subscriptions:
            self.STRIPE_SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID = {
                stripe_subscription.id: stripe_subscription
                for stripe_subscription in stripe_subscriptions
            }
            [
                self.STRIPE_SUBSCRIPTIONS_BY_STRIPE_CUSTOMER_ID[
                    stripe_subscription.customer_id
                ].append(stripe_subscription)
                for stripe_subscription in stripe_subscriptions
            ]

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

    async def get_subscription_by_stripe_customer_id(
        self, stripe_customer_id: str
    ) -> Optional[Subscription]:
        return self.SUBSCRIPTIONS_BY_CUSTOMER_ID.get(stripe_customer_id, None)

    async def get_subscription_by_user_id(self, user_id: int) -> Optional[Subscription]:
        return self.SUBSCRIPTIONS_BY_USER_ID.get(user_id, None)

    # WRITE
    async def save_subscription(self, subscription: Subscription) -> Subscription:
        self.SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID[
            subscription.stripe_subscription_id
        ] = subscription
        self.SUBSCRIPTIONS_BY_CUSTOMER_ID[
            subscription.stripe_customer_id
        ] = subscription
        self.SUBSCRIPTIONS_BY_USER_ID[subscription.user_id] = subscription
        return subscription

    # WRITE
    async def delete_subscription(self, subscription: Subscription) -> None:
        self.SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID.pop(
            subscription.stripe_subscription_id
        )
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

    async def get_payment_by_stripe_invoice_id(
        self, stripe_invoice_id: str
    ) -> SubscriptionPayment:
        return self.SUBSCRIPTION_PAYMENTS_BY_INVOICE_ID.get(stripe_invoice_id, None)

    # ============== #
    #    Stripe
    # ============== #
    async def create_checkout_session(
        self, customer_id: str
    ) -> Optional[StripeCheckoutSession]:
        return StripeCheckoutSessionFactory.build(customer_id=customer_id)

    async def retrieve_customer_portal_session_url(self, stripe_customer_id):
        return f"https://stripe.com/stripe_test_customer_portal/{stripe_customer_id}"

    async def _retrieve_customer_by_email(self, email: str) -> Optional[StripeCustomer]:
        customers = self.STRIPE_CUSTOMERS_BY_EMAIL.get(email, [])
        if len(customers) > 1:
            raise MultipleCustomerReturned()
        elif len(customers):
            return customers[0]
        return None

    async def _create_customer_by_email(self, email: str) -> Optional[StripeCustomer]:
        fake_customer = StripeCustomerFactory.build(email=email)
        self.STRIPE_CUSTOMERS_BY_EMAIL["email"] = [fake_customer]
        return fake_customer

    async def get_or_create_customer_by_email(
        self, email: str
    ) -> Optional[StripeCustomer]:
        try:
            customer: StripeCustomer = await self._retrieve_customer_by_email(email)
            if customer:
                return customer, False
        except MultipleCustomerReturned as ex:
            raise ex
        customer: StripeCustomer = await self._create_customer_by_email(email)
        return customer, True

    async def _retrieve_stripe_subscription_by_stripe_subscription_id(
        self, stripe_subscription_id: str
    ) -> Optional[StripeSubscription]:
        return self.STRIPE_SUBSCRIPTIONS_BY_STRIPE_SUBSCRIPTION_ID.get(
            stripe_subscription_id, None
        )

    async def _retrieve_stripe_subscription_by_stripe_customer_id(
        self, stripe_customer_id: str
    ) -> Optional[StripeSubscription]:
        subscriptions = self.STRIPE_SUBSCRIPTIONS_BY_STRIPE_CUSTOMER_ID.get(
            stripe_customer_id, []
        )
        subscriptions = list(
            filter(
                lambda x: x.status
                not in [
                    StripeSubscriptionStatus.CANCELED,
                    StripeSubscriptionStatus.UNPAID,
                    StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
                ],
                subscriptions,
            )
        )
        if len(subscriptions) == 1:
            return subscriptions[0]
        if len(subscriptions) > 1:
            raise MultipleCustomerSubscriptionsReturned()
        return None

    async def sync_with_external_service(
        self, subscription: Subscription, **kwargs
    ) -> Optional[Subscription]:
        stripe_subscription = None
        if subscription.stripe_subscription_id:
            stripe_subscription: StripeSubscription = (
                await self._retrieve_stripe_subscription_by_stripe_subscription_id(
                    subscription.stripe_subscription_id
                )
            )
        if not stripe_subscription:
            try:
                stripe_subscription: StripeSubscription = (
                    await self._retrieve_stripe_subscription_by_stripe_customer_id(
                        subscription.stripe_customer_id
                    )
                )
            except MultipleCustomerSubscriptionsReturned as ex:
                raise ex
        if not stripe_subscription:
            raise StripeSubscriptionNotFound()
        return subscription.sync_with_stripe_subscription(stripe_subscription)
