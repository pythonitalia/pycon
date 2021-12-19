import datetime
from datetime import timezone

import respx
import time_machine
from ward import raises, test

from src.association.tests.session import db
from src.association_membership.domain.entities import (
    PaymentStatus,
    Subscription,
    SubscriptionStatus,
)
from src.association_membership.tests.factories import SubscriptionFactory
from src.webhooks.exceptions import NoUserFoundWithEmail
from src.webhooks.handlers.pretix.pretix_event_order_paid import pretix_event_order_paid
from src.webhooks.tests.handlers.pretix.payloads import (
    CATEGORIES,
    ITEMS_WITH_CATEGORY,
    ORDER_DATA_WITH_MEMBERSHIP,
    ORDER_DATA_WITHOUT_MEMBERSHIP,
    ORDER_PAID,
)


@test("receive order paid with membership")
async def _(db=db):
    with respx.mock as mock, time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/orders/9YKZK/"
        ).respond(json=ORDER_DATA_WITH_MEMBERSHIP)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/items/?active=true&category=25"
        ).respond(json=ITEMS_WITH_CATEGORY)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/categories/"
        ).respond(json=CATEGORIES)
        mock.post("http://users-backend-url/internal-api").respond(
            json={"data": {"userByEmail": {"id": 1}}}
        )
        await pretix_event_order_paid(ORDER_PAID)

    created_subscription = await Subscription.objects.select_related(
        ["payments", "payments__pretixpayments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)

    assert created_subscription.status == SubscriptionStatus.ACTIVE
    assert created_subscription.user_id == 1
    assert len(created_subscription.payments) == 1

    payment = created_subscription.payments[0]
    assert payment.total == 1000
    assert payment.payment_date == datetime.datetime(
        2021, 12, 16, 1, 4, 43, tzinfo=timezone.utc
    )
    assert payment.period_start == datetime.datetime(
        2021, 12, 16, 1, 4, 43, tzinfo=timezone.utc
    )
    assert payment.period_end == datetime.datetime(
        2022, 12, 16, 1, 4, 43, tzinfo=timezone.utc
    )
    assert payment.status == PaymentStatus.PAID

    pretix_payment = payment.pretixpayments[0]
    assert pretix_payment.order_code == "9YKZK"
    assert pretix_payment.event_organizer == "test-organizer"
    assert pretix_payment.event_id == "local-conf-test"


@test("receive order paid twice doesn't process the payment twice")
async def _(db=db):
    with respx.mock as mock, time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/orders/9YKZK/"
        ).respond(json=ORDER_DATA_WITH_MEMBERSHIP)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/items/?active=true&category=25"
        ).respond(json=ITEMS_WITH_CATEGORY)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/categories/"
        ).respond(json=CATEGORIES)
        mock.post("http://users-backend-url/internal-api").respond(
            json={"data": {"userByEmail": {"id": 1}}}
        )
        await pretix_event_order_paid(ORDER_PAID)

        created_subscription = await Subscription.objects.select_related(
            [
                "payments",
                "payments__pretixpayments",
                "payments__stripesubscriptionpayments",
            ]
        ).get(user_id=1)

        assert created_subscription.status == SubscriptionStatus.ACTIVE
        assert len(created_subscription.payments) == 1

        await pretix_event_order_paid(ORDER_PAID)

    created_subscription = await Subscription.objects.select_related(
        ["payments", "payments__pretixpayments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)

    assert created_subscription.status == SubscriptionStatus.ACTIVE
    assert len(created_subscription.payments) == 1


@test("receive order paid without membership purchase")
async def _(db=db):
    with respx.mock as mock, time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/orders/9YKZK/"
        ).respond(json=ORDER_DATA_WITHOUT_MEMBERSHIP)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/items/?active=true&category=25"
        ).respond(json=ITEMS_WITH_CATEGORY)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/categories/"
        ).respond(json=CATEGORIES)
        mock.post("http://users-backend-url/internal-api").respond(
            json={"data": {"userByEmail": {"id": 1}}}
        )
        await pretix_event_order_paid(ORDER_PAID)

    assert not await Subscription.objects.filter(user_id=1).exists()


@test("receive order paid fails if no user maps to the email")
async def _(db=db):
    with respx.mock as mock, time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/orders/9YKZK/"
        ).respond(json=ORDER_DATA_WITH_MEMBERSHIP)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/items/?active=true&category=25"
        ).respond(json=ITEMS_WITH_CATEGORY)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/categories/"
        ).respond(json=CATEGORIES)
        mock.post("http://users-backend-url/internal-api").respond(
            json={"data": {"userByEmail": None}}
        )

        with raises(NoUserFoundWithEmail) as exc:
            await pretix_event_order_paid(ORDER_PAID)

    assert not await Subscription.objects.filter(user_id=1).exists()
    assert str(exc.raised) == "No user found with the email of order_code=9YKZK"


@test("receive order paid with canceled subscription")
async def _(db=db):
    existing_subscription = await SubscriptionFactory(
        user_id=1, status=SubscriptionStatus.CANCELED
    )

    with respx.mock as mock, time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/orders/9YKZK/"
        ).respond(json=ORDER_DATA_WITH_MEMBERSHIP)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/items/?active=true&category=25"
        ).respond(json=ITEMS_WITH_CATEGORY)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/categories/"
        ).respond(json=CATEGORIES)
        mock.post("http://users-backend-url/internal-api").respond(
            json={"data": {"userByEmail": {"id": 1}}}
        )
        await pretix_event_order_paid(ORDER_PAID)

    created_subscription = await Subscription.objects.select_related(
        ["payments", "payments__pretixpayments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)

    assert created_subscription.id == existing_subscription.id
    assert created_subscription.status == SubscriptionStatus.ACTIVE
    assert created_subscription.user_id == 1
    assert len(created_subscription.payments) == 1


@test("receive order paid of period outside current one")
async def _(db=db):
    with respx.mock as mock, time_machine.travel("2023-12-16 01:04:50Z", tick=False):
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/orders/9YKZK/"
        ).respond(json=ORDER_DATA_WITH_MEMBERSHIP)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/items/?active=true&category=25"
        ).respond(json=ITEMS_WITH_CATEGORY)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/categories/"
        ).respond(json=CATEGORIES)
        mock.post("http://users-backend-url/internal-api").respond(
            json={"data": {"userByEmail": {"id": 1}}}
        )
        await pretix_event_order_paid(ORDER_PAID)

    created_subscription = await Subscription.objects.select_related(
        ["payments", "payments__pretixpayments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)

    # We still accept the payment but we don't change to ACTIVE
    assert created_subscription.status == SubscriptionStatus.PENDING
    assert created_subscription.user_id == 1
    assert len(created_subscription.payments) == 1


@test("receive order paid of already subscribed fails with error message")
async def _(db=db):
    await SubscriptionFactory(user_id=1, status=SubscriptionStatus.ACTIVE)

    with respx.mock as mock, time_machine.travel("2023-12-16 01:04:50Z", tick=False):
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/orders/9YKZK/"
        ).respond(json=ORDER_DATA_WITH_MEMBERSHIP)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/items/?active=true&category=25"
        ).respond(json=ITEMS_WITH_CATEGORY)
        mock.get(
            "http://pretix-api/organizers/test-organizer/events/local-conf-test/categories/"
        ).respond(json=CATEGORIES)
        mock.post("http://users-backend-url/internal-api").respond(
            json={"data": {"userByEmail": {"id": 1}}}
        )

        with raises(ValueError) as exc:
            await pretix_event_order_paid(ORDER_PAID)

    created_subscription = await Subscription.objects.select_related(
        ["payments", "payments__pretixpayments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)

    # We still accept the payment but we don't change to ACTIVE
    assert created_subscription.status == SubscriptionStatus.ACTIVE
    assert len(created_subscription.payments) == 0
    assert str(exc.raised) == "User is already subscribed to the association"
