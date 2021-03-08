from zoneinfo import ZoneInfo

from association.domain import services
from association.domain.entities.subscription_entities import UserData
from association.domain.exceptions import CustomerNotAvailable
from association.domain.tests.repositories.fake_repository import (
    FakeAssociationRepository,
)
from association.tests.factories import SubscriptionFactory
from ward import raises, test

rome_tz = ZoneInfo("Europe/Rome")


@test("customer portal url returned")
async def _():
    test_stripe_customer_id = "cus_test_1234"
    repository = FakeAssociationRepository(
        subscriptions=[
            SubscriptionFactory(
                user_id=1234, stripe_customer_id=test_stripe_customer_id
            )
        ],
        customers=[],
    )

    portal_url = await services.manage_user_association_subscription(
        user_data=UserData(user_id=1234, email="pycon_tester@python.it"),
        association_repository=repository,
    )
    assert (
        portal_url
        == f"https://stripe.com/stripe_test_customer_portal/{test_stripe_customer_id}"
    )


@test("raises CustomerNotAvailable if customer not available")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[SubscriptionFactory(user_id=1234, stripe_customer_id="")],
        customers=[],
    )

    with raises(CustomerNotAvailable):
        await services.manage_user_association_subscription(
            user_data=UserData(user_id=1234, email="pycon_tester@python.it"),
            association_repository=repository,
        )
