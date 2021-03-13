import datetime
from unittest.mock import patch

import time_machine
from ward import raises, test

from association.domain import services
from association.domain.entities.stripe_entities import (
    StripeCheckoutSessionInput,
    StripeCustomer,
)
from association.domain.entities.subscription_entities import (
    SubscriptionState,
    UserData,
)
from association.domain.exceptions import AlreadySubscribed
from association.domain.tests.repositories.fake_repository import (
    FakeAssociationRepository,
)
from association.tests.factories import (
    StripeCheckoutSessionFactory,
    SubscriptionFactory,
)


@test("NEW subscription")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    with time_machine.travel("2021-03-13 13:00:00", tick=False):
        subscription = await services.subscribe_user_to_association(
            user_data=UserData(email="test_user@pycon.it", user_id=1357),
            association_repository=repository,
        )

        assert subscription.stripe_session_id != ""
        assert subscription.stripe_customer_id == ""
        assert subscription.state == SubscriptionState.PENDING
        assert subscription.user_id == 1357
        assert subscription.user_email == "test_user@pycon.it"
        assert subscription.creation_date == datetime.datetime(2021, 3, 13, 13, 0)


@test("OLD subscription returned if not paid and with session_id")
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357, state=SubscriptionState.PENDING
    )

    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="test_user@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription.user_id == 1357
    assert orig_subscription.stripe_session_id != ""
    assert subscription.stripe_session_id == orig_subscription.stripe_session_id


@test(
    "Old subscription returned with a new stripe_session_id if not paid and without session_id"
)
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357, state=SubscriptionState.NOT_CREATED
    )

    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="test_user@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription.user_id == 1357
    assert subscription.stripe_session_id != orig_subscription.stripe_session_id


@test("raises AlreadySubscribed if paid but not expired")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[
            SubscriptionFactory(user_id=1357, state=SubscriptionState.ACTIVE)
        ],
        customers=[],
    )
    with raises(AlreadySubscribed):
        await services.subscribe_user_to_association(
            user_data=UserData(email="test_user@pycon.it", user_id=1357),
            association_repository=repository,
        )


@test("raises AlreadySubscribed if paid and expired")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[
            SubscriptionFactory(user_id=1357, state=SubscriptionState.EXPIRED)
        ],
        customers=[],
    )
    with raises(AlreadySubscribed):
        await services.subscribe_user_to_association(
            user_data=UserData(email="test_user@pycon.it", user_id=1357),
            association_repository=repository,
        )


@test("create new checkout session with old customer")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[],
        customers=[
            StripeCustomer(id="cus_test_12345", email="old_stripe_customer@pycon.it")
        ],
    )

    with patch.object(
        repository,
        "create_checkout_session",
        return_value=StripeCheckoutSessionFactory.build(),
    ) as create_checkout_session_mock:
        await services.subscribe_user_to_association(
            user_data=UserData(email="old_stripe_customer@pycon.it", user_id=1357),
            association_repository=repository,
        )
        create_checkout_session_mock.assert_called_once_with(
            StripeCheckoutSessionInput(
                customer_email="old_stripe_customer@pycon.it",
                customer_id="cus_test_12345",
            )
        )


@test("return new checkout session with old customer")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[],
        customers=[
            StripeCustomer(id="cus_test_12345", email="old_stripe_customer@pycon.it")
        ],
    )

    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="old_stripe_customer@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription.stripe_customer_id == "cus_test_12345"


@test("create new checkout session without customer")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    with patch.object(
        repository,
        "create_checkout_session",
        return_value=StripeCheckoutSessionFactory.build(),
    ) as create_checkout_session_mock:
        await services.subscribe_user_to_association(
            user_data=UserData(email="old_stripe_customer@pycon.it", user_id=1357),
            association_repository=repository,
        )
        create_checkout_session_mock.assert_called_once_with(
            StripeCheckoutSessionInput(
                customer_email="old_stripe_customer@pycon.it", customer_id=""
            )
        )


@test("return new checkout session without customer")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="old_stripe_customer@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription.stripe_customer_id == ""
