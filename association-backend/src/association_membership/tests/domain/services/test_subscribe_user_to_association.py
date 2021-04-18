from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo
from ward import raises, test

from src.association_membership.domain.entities import Subscription, SubscriptionStatus
from src.association_membership.domain.exceptions import AlreadySubscribed
from src.association_membership.domain.services.subscribe_user_to_association import (
    subscribe_user_to_association,
)
from src.association_membership.tests.fake_repository import (
    FakeAssociationMembershipRepository,
)
from src.customers.domain.entities import Customer
from src.customers.tests.fake_repository import FakeCustomersRepository


@test("subscribe user without existing customer profile")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it")

    checkout_session_id = await subscribe_user_to_association(
        user,
        customers_repository=FakeCustomersRepository(),
        association_repository=FakeAssociationMembershipRepository(),
    )
    assert checkout_session_id == "cs_session_cus_test_1"


@test("subscribe user with active subscription fails")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it")
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
    fake_customers_repository = FakeCustomersRepository(customers=[customer])

    with raises(AlreadySubscribed):
        await subscribe_user_to_association(
            user,
            customers_repository=fake_customers_repository,
            association_repository=FakeAssociationMembershipRepository(),
        )


@test("subscribe user with canceled subscription works")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it")
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
    fake_customers_repository = FakeCustomersRepository(customers=[customer])

    checkout_session_id = await subscribe_user_to_association(
        user,
        customers_repository=fake_customers_repository,
        association_repository=FakeAssociationMembershipRepository(),
    )
    assert checkout_session_id == "cs_session_cus_hello"
