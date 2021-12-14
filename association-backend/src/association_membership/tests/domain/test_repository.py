from datetime import datetime, timezone
from unittest.mock import patch

from ward import raises, test

from src.association.settings import STRIPE_SUBSCRIPTION_PRICE_ID
from src.association.tests.session import db

from src.association_membership.domain.repository import AssociationMembershipRepository
from src.association_membership.tests.factories import SubscriptionFactory


@test("get user subscription")
async def _(db=db):
    subscription = await SubscriptionFactory(user_id=1)

    repository = AssociationMembershipRepository()
    found_subscription = await repository.get_user_subscription(1)

    assert found_subscription.id == subscription.id
