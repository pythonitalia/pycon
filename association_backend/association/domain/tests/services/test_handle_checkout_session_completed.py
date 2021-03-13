from ward import raises, test

from association.domain import services
from association.domain.exceptions import SubscriptionNotUpdated
from association.domain.services import SubscriptionUpdateInput
from association.domain.tests.repositories.fake_repository import (
    FakeAssociationRepository,
)
from association.tests.factories import SubscriptionFactory


@test("Subscription updated with customer and subscription")
async def _():
    sut_subscription = SubscriptionFactory(
        stripe_session_id="cs_test_12345", stripe_id="", stripe_customer_id=""
    )
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_checkout_session_completed(
        data=SubscriptionUpdateInput(
            session_id="cs_test_12345",
            subscription_id="sub_test_12345",
            customer_id="cus_test_12345",
        ),
        association_repository=repository,
    )

    assert subscription.stripe_session_id == sut_subscription.stripe_session_id
    assert subscription.state == sut_subscription.state
    assert subscription.stripe_id == "sub_test_12345"
    assert subscription.stripe_customer_id == "cus_test_12345"


@test("SubscriptionNotUpdated raised")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    with raises(SubscriptionNotUpdated):
        await services.handle_checkout_session_completed(
            data=SubscriptionUpdateInput(
                session_id="cs_test_12345",
                subscription_id="sub_test_12345",
                customer_id="cus_test_12345",
            ),
            association_repository=repository,
        )
