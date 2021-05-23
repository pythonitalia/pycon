from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo
from ward import raises, test

from src.association_membership.domain.entities import Subscription, SubscriptionStatus
from src.association_membership.domain.exceptions import (
    CustomerNotAvailable,
    NoSubscriptionAvailable,
)
from src.association_membership.domain.services.manage_user_association_subscription import (
    manage_user_association_subscription,
)
from src.customers.domain.entities import Customer
from src.customers.tests.fake_repository import FakeCustomersRepository


@test("manage subscription user")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    customer = Customer(
        id=1,
        user_id=1,
        stripe_customer_id="cus_hello",
    )
    customer.subscriptions = [
        Subscription(
            id=1,
            customer=customer,
            stripe_subscription_id="sub_1",
            status=SubscriptionStatus.ACTIVE,
        )
    ]

    fake_repository = FakeCustomersRepository(customers=[customer])

    billing_portal_url = await manage_user_association_subscription(
        user, customers_repository=fake_repository
    )

    assert billing_portal_url == "https://fake.stripe/customerportal/cus_hello"


@test("fails if the user doesnt have an active subscription")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    customer = Customer(
        id=1,
        user_id=1,
        stripe_customer_id="cus_hello",
    )
    customer.subscriptions = [
        Subscription(
            id=1,
            customer=customer,
            stripe_subscription_id="sub_1",
            status=SubscriptionStatus.CANCELED,
        )
    ]

    fake_repository = FakeCustomersRepository(customers=[customer])

    with raises(NoSubscriptionAvailable):
        await manage_user_association_subscription(
            user, customers_repository=fake_repository
        )


@test("fails if the user doesnt have any subscription")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    customer = Customer(
        id=1,
        user_id=1,
        stripe_customer_id="cus_hello",
    )
    customer.subscriptions = []

    fake_repository = FakeCustomersRepository(customers=[customer])

    with raises(NoSubscriptionAvailable):
        await manage_user_association_subscription(
            user, customers_repository=fake_repository
        )


@test("fails if the user doesnt have a customer")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    customer = Customer(
        id=1,
        user_id=3,
        stripe_customer_id="cus_hello",
    )
    customer.subscriptions = []
    fake_repository = FakeCustomersRepository(customers=[customer])

    with raises(CustomerNotAvailable):
        await manage_user_association_subscription(
            user, customers_repository=fake_repository
        )
