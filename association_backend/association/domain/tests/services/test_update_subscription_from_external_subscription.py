from unittest.mock import patch

from ward import raises, test

from association.domain import services
from association.domain.entities.stripe import StripeStatus
from association.domain.entities.subscriptions import SubscriptionState
from association.domain.exceptions import (
    InconsistentStateTransitionError,
    SubscriptionNotFound,
)
from association.domain.services.update_subscription_from_external_subscription import (
    SubscriptionDetailInput,
)
from association.domain.tests.repositories.fake_repository import (
    FakeAssociationRepository,
)
from association.tests.factories import SubscriptionFactory, SubscriptionPaymentFactory


@test("Subscription updated ACTIVE")
async def _():
    sut_subscription = SubscriptionFactory(
        stripe_subscription_id="sub_test_1234", state=SubscriptionState.EXPIRED
    )
    assert sut_subscription.stripe_subscription_id == "sub_test_1234"
    assert sut_subscription.state == SubscriptionState.EXPIRED

    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.update_subscription_from_external_subscription(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_subscription_id,
            status=StripeStatus.ACTIVE,
        ),
        subscription=None,
        association_repository=repository,
    )

    assert (
        subscription.stripe_subscription_id == sut_subscription.stripe_subscription_id
    )
    assert subscription.state == SubscriptionState.ACTIVE


@test("Subscription if passed doesn't hit db")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])
    with patch(
        "association.domain.repositories.association_repository.AssociationRepository.get_subscription_by_stripe_subscription_id",
        return_value=SubscriptionFactory(),
    ) as method_mock:
        await services.update_subscription_from_external_subscription(
            data=SubscriptionDetailInput(
                subscription_id=SubscriptionFactory.build().stripe_subscription_id,
                status=StripeStatus.ACTIVE,
            ),
            subscription=SubscriptionFactory(),
            association_repository=repository,
        )
        method_mock.assert_not_called()


@test("SubscriptionNotFound raised")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    with raises(SubscriptionNotFound):
        await services.update_subscription_from_external_subscription(
            data=SubscriptionDetailInput(
                subscription_id=SubscriptionFactory.build().stripe_subscription_id,
                status=StripeStatus.ACTIVE,
            ),
            subscription=None,
            association_repository=repository,
        )


@test("Subscription update does not raise if status changes")
async def _():
    sut_subscription = SubscriptionFactory(
        stripe_subscription_id="sub_test_1234", state=SubscriptionState.ACTIVE
    )
    assert sut_subscription.stripe_subscription_id == "sub_test_1234"
    assert sut_subscription.state == SubscriptionState.ACTIVE

    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.update_subscription_from_external_subscription(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_subscription_id,
            status=StripeStatus.ACTIVE,
        ),
        subscription=None,
        association_repository=repository,
    )

    assert (
        subscription.stripe_subscription_id == sut_subscription.stripe_subscription_id
    )
    assert subscription.state == SubscriptionState.ACTIVE


@test("Subscription update ACTIVE")
async def _():
    sut_subscription = SubscriptionFactory()
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.update_subscription_from_external_subscription(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_subscription_id,
            status=StripeStatus.ACTIVE,
        ),
        subscription=None,
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.ACTIVE


@test("Subscription update INCOMPLETE -> PENDING")
async def _():
    sut_subscription = SubscriptionFactory()
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.update_subscription_from_external_subscription(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_subscription_id,
            status=StripeStatus.INCOMPLETE,
        ),
        subscription=None,
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.PENDING


@test(
    "Subscription update INCOMPLETE_EXPIRED -> FIRST_PAYMENT_EXPIRED + Deleted session_id & subscription_id"
)
async def _():
    sut_subscription = SubscriptionFactory(state=SubscriptionState.PENDING)
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    assert sut_subscription.stripe_session_id != ""
    assert sut_subscription.stripe_subscription_id != ""

    subscription = await services.update_subscription_from_external_subscription(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_subscription_id,
            status=StripeStatus.INCOMPLETE_EXPIRED,
        ),
        subscription=None,
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.FIRST_PAYMENT_EXPIRED
    assert subscription.stripe_session_id == ""
    assert subscription.stripe_subscription_id == ""


@test(
    "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription state is ACTIVE"
)
async def _():
    sut_subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    assert sut_subscription.stripe_session_id != ""

    with raises(InconsistentStateTransitionError):
        await services.update_subscription_from_external_subscription(
            data=SubscriptionDetailInput(
                subscription_id=sut_subscription.stripe_subscription_id,
                status=StripeStatus.INCOMPLETE_EXPIRED,
            ),
            subscription=None,
            association_repository=repository,
        )


@test(
    "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription state is EXPIRED"
)
async def _():
    sut_subscription = SubscriptionFactory(state=SubscriptionState.EXPIRED)
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    assert sut_subscription.stripe_session_id != ""

    with raises(InconsistentStateTransitionError):
        await services.update_subscription_from_external_subscription(
            data=SubscriptionDetailInput(
                subscription_id=sut_subscription.stripe_subscription_id,
                status=StripeStatus.INCOMPLETE_EXPIRED,
            ),
            subscription=None,
            association_repository=repository,
        )


@test(
    "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription has associated Payments"
)
async def _():
    sut_subscription = SubscriptionFactory(state=SubscriptionState.PENDING)
    subscription_payment = SubscriptionPaymentFactory(subscription=sut_subscription)
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription],
        customers=[],
        subscription_payments=[subscription_payment],
    )

    assert sut_subscription.stripe_session_id != ""

    with raises(InconsistentStateTransitionError):
        await services.update_subscription_from_external_subscription(
            data=SubscriptionDetailInput(
                subscription_id=sut_subscription.stripe_subscription_id,
                status=StripeStatus.INCOMPLETE_EXPIRED,
            ),
            subscription=None,
            association_repository=repository,
        )


@test("Subscription update CANCELED -> CANCELED + Deleted session_id & subscription_id")
async def _():
    sut_subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    assert sut_subscription.stripe_session_id != ""
    assert sut_subscription.stripe_subscription_id != ""

    subscription = await services.update_subscription_from_external_subscription(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_subscription_id,
            status=StripeStatus.CANCELED,
        ),
        subscription=None,
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.CANCELED
    assert subscription.stripe_session_id == ""
    assert subscription.stripe_subscription_id == ""


@test("Subscription update UNPAID -> CANCELED + Deleted session_id & subscription_id")
async def _():
    sut_subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    assert sut_subscription.stripe_session_id != ""
    assert sut_subscription.stripe_subscription_id != ""

    subscription = await services.update_subscription_from_external_subscription(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_subscription_id,
            status=StripeStatus.UNPAID,
        ),
        subscription=None,
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.CANCELED
    assert subscription.stripe_session_id == ""
    assert subscription.stripe_subscription_id == ""


@test("Subscription update PAST_DUE -> EXPIRED")
async def _():
    sut_subscription = SubscriptionFactory()
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.update_subscription_from_external_subscription(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_subscription_id,
            status=StripeStatus.PAST_DUE,
        ),
        subscription=None,
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.EXPIRED
