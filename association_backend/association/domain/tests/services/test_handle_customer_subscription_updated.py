from ward import raises, test

from association.domain import services
from association.domain.entities.stripe import StripeStatus
from association.domain.entities.subscriptions import SubscriptionState
from association.domain.exceptions import (
    InconsistentStateTransitionError,
    SubscriptionNotFound,
)
from association.domain.services.handle_customer_subscription_updated import (
    SubscriptionDetailInput,
)
from association.domain.tests.repositories.fake_repository import (
    FakeAssociationRepository,
)
from association.tests.factories import SubscriptionFactory, SubscriptionPaymentFactory


@test("Subscription updated ACTIVE")
async def _():
    sut_subscription = SubscriptionFactory(
        stripe_id="sub_test_1234", state=SubscriptionState.EXPIRED
    )
    assert sut_subscription.stripe_id == "sub_test_1234"
    assert sut_subscription.state == SubscriptionState.EXPIRED

    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_customer_subscription_updated(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_id, status=StripeStatus.ACTIVE
        ),
        association_repository=repository,
    )

    assert subscription.stripe_id == sut_subscription.stripe_id
    assert subscription.state == SubscriptionState.ACTIVE


@test("SubscriptionNotFound raised")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    with raises(SubscriptionNotFound):
        await services.handle_customer_subscription_updated(
            data=SubscriptionDetailInput(
                subscription_id=SubscriptionFactory.build().stripe_id,
                status=StripeStatus.ACTIVE,
            ),
            association_repository=repository,
        )


@test("Subscription update does not raise if status changes")
async def _():
    sut_subscription = SubscriptionFactory(
        stripe_id="sub_test_1234", state=SubscriptionState.ACTIVE
    )
    assert sut_subscription.stripe_id == "sub_test_1234"
    assert sut_subscription.state == SubscriptionState.ACTIVE

    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_customer_subscription_updated(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_id, status=StripeStatus.ACTIVE
        ),
        association_repository=repository,
    )

    assert subscription.stripe_id == sut_subscription.stripe_id
    assert subscription.state == SubscriptionState.ACTIVE


@test("Subscription update ACTIVE")
async def _():
    sut_subscription = SubscriptionFactory()
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_customer_subscription_updated(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_id, status=StripeStatus.ACTIVE
        ),
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.ACTIVE


@test("Subscription update INCOMPLETE -> PENDING")
async def _():
    sut_subscription = SubscriptionFactory()
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_customer_subscription_updated(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_id, status=StripeStatus.INCOMPLETE
        ),
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.PENDING


@test("Subscription update INCOMPLETE_EXPIRED -> NOT_CREATED + Deleted session")
async def _():
    sut_subscription = SubscriptionFactory(state=SubscriptionState.PENDING)
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    assert sut_subscription.stripe_session_id != ""
    assert sut_subscription.stripe_id != ""

    subscription = await services.handle_customer_subscription_updated(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_id,
            status=StripeStatus.INCOMPLETE_EXPIRED,
        ),
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.NOT_CREATED
    assert subscription.stripe_session_id == ""
    assert subscription.stripe_id == ""


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
        await services.handle_customer_subscription_updated(
            data=SubscriptionDetailInput(
                subscription_id=sut_subscription.stripe_id,
                status=StripeStatus.INCOMPLETE_EXPIRED,
            ),
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
        await services.handle_customer_subscription_updated(
            data=SubscriptionDetailInput(
                subscription_id=sut_subscription.stripe_id,
                status=StripeStatus.INCOMPLETE_EXPIRED,
            ),
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
        await services.handle_customer_subscription_updated(
            data=SubscriptionDetailInput(
                subscription_id=sut_subscription.stripe_id,
                status=StripeStatus.INCOMPLETE_EXPIRED,
            ),
            association_repository=repository,
        )


@test("Subscription update PAST_DUE -> EXPIRED")
async def _():
    sut_subscription = SubscriptionFactory()
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_customer_subscription_updated(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_id, status=StripeStatus.PAST_DUE
        ),
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.EXPIRED


@test("Subscription update CANCELED -> EXPIRED")
async def _():
    sut_subscription = SubscriptionFactory()
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_customer_subscription_updated(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_id, status=StripeStatus.CANCELED
        ),
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.EXPIRED


@test("Subscription update UNPAID -> EXPIRED")
async def _():
    sut_subscription = SubscriptionFactory()
    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_customer_subscription_updated(
        data=SubscriptionDetailInput(
            subscription_id=sut_subscription.stripe_id, status=StripeStatus.UNPAID
        ),
        association_repository=repository,
    )

    assert subscription.state == SubscriptionState.EXPIRED
