from ward import test

from association.domain import services
from association.domain.entities import SubscriptionState
from association.domain.tests.repositories.fake_repository import (
    FakeAssociationRepository,
)
from association.tests.factories import SubscriptionFactory


@test("return has_association_subscription False if no subscription")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[],
        customers=[],
    )

    assert (
        await services.user_has_association_subscription(
            user_id=1234,
            association_repository=repository,
        )
        is False
    )


@test("return has_association_subscription False if subscription PENDING")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[
            SubscriptionFactory(user_id=1234, state=SubscriptionState.PENDING)
        ],
        customers=[],
    )

    assert (
        await services.user_has_association_subscription(
            user_id=1234,
            association_repository=repository,
        )
        is False
    )


@test("return has_association_subscription False if subscription FIRST_PAYMENT_EXPIRED")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[
            SubscriptionFactory(
                user_id=1234, state=SubscriptionState.FIRST_PAYMENT_EXPIRED
            )
        ],
        customers=[],
    )

    assert (
        await services.user_has_association_subscription(
            user_id=1234,
            association_repository=repository,
        )
        is False
    )


@test("return has_association_subscription True if subscription ACTIVE")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[
            SubscriptionFactory(user_id=1234, state=SubscriptionState.ACTIVE)
        ],
        customers=[],
    )

    assert (
        await services.user_has_association_subscription(
            user_id=1234,
            association_repository=repository,
        )
        is True
    )


@test("return has_association_subscription True if subscription EXPIRED")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[
            SubscriptionFactory(user_id=1234, state=SubscriptionState.EXPIRED)
        ],
        customers=[],
    )

    assert (
        await services.user_has_association_subscription(
            user_id=1234,
            association_repository=repository,
        )
        is True
    )
