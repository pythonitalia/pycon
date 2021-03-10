import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

import time_machine
from ward import raises, test

from association.domain import services
from association.domain.entities.stripe_entities import (
    StripeCheckoutSessionInput,
    StripeCustomer,
)
from association.domain.entities.subscription_entities import (
    Subscription,
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

rome_tz = ZoneInfo("Europe/Rome")


@test("NEW subscription")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    with time_machine.travel(datetime.datetime(2020, 1, 1, tzinfo=rome_tz), tick=False):
        subscription = await services.subscribe_user_to_association(
            user_data=UserData(email="g.donghia@mailinator.com", user_id=1357),
            association_repository=repository,
        )

        assert subscription.stripe_session_id != ""
        assert subscription.stripe_customer_id == ""
        assert subscription.state == SubscriptionState.PENDING
        assert subscription.user_id == 1357
        assert subscription.creation_date == datetime.datetime(2020, 1, 1, 0, 0)


@test("OLD subscription returned if not paid")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[SubscriptionFactory(user_id=1357)], customers=[]
    )

    with patch.object(
        Subscription, "get_calculated_state", return_value=SubscriptionState.PENDING
    ) as state_mock:
        subscription = await services.subscribe_user_to_association(
            user_data=UserData(email="g.donghia@mailinator.com", user_id=1357),
            association_repository=repository,
        )
        assert subscription.user_id == 1357
        state_mock.assert_called()


@test("raises AlreadySubscribed if paid but not expired")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[SubscriptionFactory(user_id=1357)], customers=[]
    )

    with patch.object(
        Subscription, "get_calculated_state", return_value=SubscriptionState.ACTIVE
    ) as state_mock:
        with raises(AlreadySubscribed):
            subscription = await services.subscribe_user_to_association(
                user_data=UserData(email="g.donghia@mailinator.com", user_id=1357),
                association_repository=repository,
            )
            assert subscription.user_id == 1357
            state_mock.assert_called()


@test("return old checkout session with old subscription if subscription expired")
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[SubscriptionFactory(user_id=1357, stripe_id="sub_test_7890")],
        customers=[],
    )

    with patch.object(
        Subscription, "get_calculated_state", return_value=SubscriptionState.EXPIRED
    ) as state_mock:
        with raises(AlreadySubscribed):
            subscription = await services.subscribe_user_to_association(
                user_data=UserData(email="g.donghia@mailinator.com", user_id=1357),
                association_repository=repository,
            )
            assert subscription.user_id == 1357
            state_mock.assert_called()


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
