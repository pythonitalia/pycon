import datetime
from unittest.mock import patch

import time_machine
from ward import raises, test

from association.domain import services
from association.domain.entities.stripe import (
    StripeCheckoutSession,
    StripeCheckoutSessionInput,
    StripeCustomer,
    StripeStatus,
    StripeSubscription,
)
from association.domain.entities.subscriptions import SubscriptionState, UserData
from association.domain.exceptions import AlreadySubscribed, MultipleCustomerReturned
from association.domain.tests.repositories.fake_repository import (
    FakeAssociationRepository,
)
from association.tests.factories import (
    StripeCheckoutSessionFactory,
    SubscriptionFactory,
)


@test("No Subscription -> return New Subscription without customer")
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
        assert subscription.creation_date == datetime.datetime(2021, 3, 13, 13, 0)


@test("subscription PENDING with stripe_subscription -> returns self")
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357, state=SubscriptionState.PENDING, stripe_session_id="cs_test_12347"
    )
    assert orig_subscription.stripe_subscription_id != ""

    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="test_user@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription.user_id == 1357
    assert subscription.stripe_session_id == "cs_test_12347"


@test(
    "subscription PENDING without stripe_subscription -> returns changed subscription"
)
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357, without_subscription=True, stripe_session_id="cs_test_12345"
    )
    assert orig_subscription.stripe_subscription_id == ""

    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription],
        customers=[],
        checkout_sessions=[
            StripeCheckoutSession(
                id="cs_test_12345",
                customer_id=SubscriptionFactory.build().stripe_customer_id,
                subscription_id="sub_test_12345",
            )
        ],
        stripe_subscriptions=[
            StripeSubscription(
                id="sub_test_12345",
                status=StripeStatus.INCOMPLETE_EXPIRED,
                customer_id="cus_test_12345",
            )
        ],
    )
    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="test_user@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription.user_id == 1357
    assert subscription.stripe_session_id != "cs_test_12345"


@test("subscription ACTIVE -> raises AlreadySubscribed")
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


@test("subscription EXPIRED -> raises AlreadySubscribed")
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


@test(
    "subscription FIRST_PAYMENT_EXPIRED -> returns OLD Subscription with new Session ID"
)
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357,
        state=SubscriptionState.FIRST_PAYMENT_EXPIRED,
        stripe_session_id="cs_test_12345",
    )
    assert orig_subscription.stripe_session_id == "cs_test_12345"
    print(f"{orig_subscription.stripe_session_id = }")
    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="test_user@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription == orig_subscription
    assert subscription.user_id == 1357
    assert subscription.stripe_session_id != "cs_test_12345"


@test("subscription CANCELED -> returns OLD Subscription with new Session ID")
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357,
        state=SubscriptionState.CANCELED,
        stripe_session_id="cs_test_12345",
    )
    assert orig_subscription.stripe_session_id == "cs_test_12345"
    print(f"{orig_subscription.stripe_session_id = }")
    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="test_user@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription == orig_subscription
    assert subscription.user_id == 1357
    assert subscription.stripe_session_id != "cs_test_12345"


@test(
    "No Subscription but Existing Customer -> calls AssociationRepository.create_checkout_session passing existing customer_id"
)
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


@test(
    "No Subscription but more than 1 Existing Customers with same email -> raises MultipleCustomerReturned"
)
async def _():
    repository = FakeAssociationRepository(
        subscriptions=[],
        customers=[
            StripeCustomer(id="cus_test_12345", email="old_stripe_customer@pycon.it"),
            StripeCustomer(id="cus_test_12346", email="old_stripe_customer@pycon.it"),
        ],
    )
    with raises(MultipleCustomerReturned):
        await services.subscribe_user_to_association(
            user_data=UserData(email="old_stripe_customer@pycon.it", user_id=1357),
            association_repository=repository,
        )


@test("No Subscription -> calls AssociationRepository.create_checkout_session")
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


@test("No Subscription -> calls AssociationRepository.save_subscription")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    with patch.object(
        repository,
        "save_subscription",
        return_value=SubscriptionFactory.build(),
    ) as save_subscription_mock:
        await services.subscribe_user_to_association(
            user_data=UserData(email="old_stripe_customer@pycon.it", user_id=1357),
            association_repository=repository,
        )
        save_subscription_mock.assert_called_once()


@test(
    "No Subscription but Existing Customer -> returns New Subscription with that customer"
)
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


@test(
    "subscription FIRST_PAYMENT_EXPIRED without customer -> calls AssociationRepository.create_checkout_session with empty customer_id"
)
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357,
        state=SubscriptionState.FIRST_PAYMENT_EXPIRED,
        stripe_customer_id="",
    )
    assert orig_subscription.stripe_session_id != ""
    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    with patch.object(
        repository,
        "create_checkout_session",
        return_value=StripeCheckoutSessionFactory.build(),
    ) as create_checkout_session_mock:
        await services.subscribe_user_to_association(
            user_data=UserData(email="test_user@pycon.it", user_id=1357),
            association_repository=repository,
        )
        create_checkout_session_mock.assert_called_once_with(
            StripeCheckoutSessionInput(
                customer_email="test_user@pycon.it", customer_id=""
            )
        )


@test(
    "subscription FIRST_PAYMENT_EXPIRED with customer -> calls AssociationRepository.create_checkout_session with customer.customer_id"
)
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357,
        # state=SubscriptionState.FIRST_PAYMENT_EXPIRED,
        without_manageable_subscription=True,
        stripe_customer_id="cus_test_12345",
    )
    assert orig_subscription.stripe_session_id != ""
    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    with patch.object(
        repository,
        "create_checkout_session",
        return_value=StripeCheckoutSessionFactory.build(),
    ) as create_checkout_session_mock:
        await services.subscribe_user_to_association(
            user_data=UserData(email="test_user@pycon.it", user_id=1357),
            association_repository=repository,
        )
        create_checkout_session_mock.assert_called_once_with(
            StripeCheckoutSessionInput(
                customer_email="test_user@pycon.it", customer_id="cus_test_12345"
            )
        )


@test(
    "subscription FIRST_PAYMENT_EXPIRED -> calls AssociationRepository.save_subscription with old subscription"
)
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357, state=SubscriptionState.FIRST_PAYMENT_EXPIRED
    )
    assert orig_subscription.stripe_session_id != ""
    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    with patch.object(
        repository,
        "save_subscription",
        return_value=None,
    ) as save_subscription_mock:
        await services.subscribe_user_to_association(
            user_data=UserData(email="test_user@pycon.it", user_id=1357),
            association_repository=repository,
        )
        save_subscription_mock.assert_called_once_with(orig_subscription)


@test(
    "subscription FIRST_PAYMENT_EXPIRED -> calls AssociationRepository.save_subscription"
)
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357, state=SubscriptionState.FIRST_PAYMENT_EXPIRED
    )
    assert orig_subscription.stripe_session_id != ""
    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription], customers=[]
    )

    with patch.object(
        repository,
        "save_subscription",
        return_value=SubscriptionFactory.build(),
    ) as save_subscription_mock:
        await services.subscribe_user_to_association(
            user_data=UserData(email="old_stripe_customer@pycon.it", user_id=1357),
            association_repository=repository,
        )
        save_subscription_mock.assert_called_once()


@test(
    "subscription FIRST_PAYMENT_EXPIRED with Existing Customer -> returns New Subscription with that customer"
)
async def _():
    orig_subscription = SubscriptionFactory(
        user_id=1357,
        state=SubscriptionState.FIRST_PAYMENT_EXPIRED,
        stripe_customer_id="cus_test_12345",
    )
    assert orig_subscription.stripe_session_id != ""
    repository = FakeAssociationRepository(
        subscriptions=[orig_subscription],
        customers=[
            StripeCustomer(id="cus_test_12345", email="old_stripe_customer@pycon.it")
        ],
    )

    subscription = await services.subscribe_user_to_association(
        user_data=UserData(email="new_customer_email@pycon.it", user_id=1357),
        association_repository=repository,
    )
    assert subscription.stripe_customer_id == "cus_test_12345"
