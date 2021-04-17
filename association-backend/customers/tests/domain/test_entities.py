from ward import test

from association_membership.domain.entities import Subscription, SubscriptionStatus
from customers.domain.entities import Customer


@test("customer has active subscriptions")
async def _():
    customer = Customer(id=1, user_id=1, stripe_customer_id="cus_1")
    customer.subscriptions = [
        Subscription(
            id=1,
            customer=customer,
            stripe_subscription_id="sub_1",
            status=SubscriptionStatus.ACTIVE,
        )
    ]

    assert customer.has_active_subscription() is True


@test("customer with all canceled subscriptions")
async def _():
    customer = Customer(id=1, user_id=1, stripe_customer_id="cus_1")
    customer.subscriptions = [
        Subscription(
            id=1,
            customer=customer,
            stripe_subscription_id="sub_1",
            status=SubscriptionStatus.CANCELED,
        ),
        Subscription(
            id=2,
            customer=customer,
            stripe_subscription_id="sub_2",
            status=SubscriptionStatus.CANCELED,
        ),
    ]

    assert customer.has_active_subscription() is False


@test("customer with active and canceled subscription")
async def _():
    customer = Customer(id=1, user_id=1, stripe_customer_id="cus_1")
    customer.subscriptions = [
        Subscription(
            id=1,
            customer=customer,
            stripe_subscription_id="sub_1",
            status=SubscriptionStatus.ACTIVE,
        ),
        Subscription(
            id=2,
            customer=customer,
            stripe_subscription_id="sub_2",
            status=SubscriptionStatus.CANCELED,
        ),
    ]

    assert customer.has_active_subscription() is True


@test("customer no active subscription with no subscription")
async def _():
    customer = Customer(id=1, user_id=1, stripe_customer_id="cus_1")
    customer.subscriptions = []

    assert customer.has_active_subscription() is False
