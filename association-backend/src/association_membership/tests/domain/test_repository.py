from ward import test

from src.association.tests.session import db
from src.association_membership.domain.repository import AssociationMembershipRepository
from src.association_membership.tests.factories import (
    StripeCustomerFactory,
    SubscriptionFactory,
)


@test("get user subscription")
async def _(db=db):
    subscription = await SubscriptionFactory(user_id=1)

    repository = AssociationMembershipRepository()
    found_subscription = await repository.get_user_subscription(1)

    assert found_subscription.id == subscription.id


@test("get stripe customer from user id")
async def _(db=db):
    customer = await StripeCustomerFactory(user_id=1)

    repository = AssociationMembershipRepository()
    found_customer = await repository.get_stripe_customer_from_user_id(1)

    assert found_customer.id == customer.id
