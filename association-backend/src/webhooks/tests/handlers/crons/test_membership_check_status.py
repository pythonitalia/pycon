import datetime
from datetime import timezone

import time_machine
from ward import test

from src.association.tests.session import db
from src.association_membership.domain.entities import (
    PaymentStatus,
    Subscription,
    SubscriptionStatus,
)
from src.association_membership.domain.repository import AssociationMembershipRepository
from src.association_membership.tests.factories import SubscriptionFactory
from src.webhooks.handlers.crons.membership_check_status import membership_check_status


@test("with no expired subscriptions")
async def _(db=db):
    repository = AssociationMembershipRepository()
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.ACTIVE
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        subscription_2 = await SubscriptionFactory(
            user_id=2, status=SubscriptionStatus.ACTIVE
        )
        subscription_2.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="AABBCC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
        )

        await repository.save_subscription(subscription_1)
        await repository.save_subscription(subscription_2)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE

        updated_subscription_2 = await Subscription.objects.get_or_none(
            id=subscription_2.id
        )
        assert updated_subscription_2.status == SubscriptionStatus.ACTIVE


@test("with one expired subscription")
async def _(db=db):
    repository = AssociationMembershipRepository()

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.ACTIVE
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        subscription_2 = await SubscriptionFactory(
            user_id=2, status=SubscriptionStatus.ACTIVE
        )
        subscription_2.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="AABBCC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
        )

        await repository.save_subscription(subscription_1)
        await repository.save_subscription(subscription_2)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE

        # The only payment of subscription 2 is until 2020-05-05.
        # Current time is 2020-10-10.
        updated_subscription_2 = await Subscription.objects.get_or_none(
            id=subscription_2.id
        )
        assert updated_subscription_2.status == SubscriptionStatus.CANCELED


@test("subscription that is canceled but has a payment for this range is activated")
async def _(db=db):
    repository = AssociationMembershipRepository()

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.CANCELED
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        subscription_2 = await SubscriptionFactory(
            user_id=2, status=SubscriptionStatus.CANCELED
        )
        subscription_2.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="AABBCC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
        )

        await repository.save_subscription(subscription_1)
        await repository.save_subscription(subscription_2)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE

        updated_subscription_2 = await Subscription.objects.get_or_none(
            id=subscription_2.id
        )
        assert updated_subscription_2.status == SubscriptionStatus.CANCELED


@test("subscription with multiple payments")
async def _(db=db):
    repository = AssociationMembershipRepository()

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.ACTIVE
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2022, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        await repository.save_subscription(subscription_1)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


@test("subscription with overlapping payments")
async def _(db=db):
    repository = AssociationMembershipRepository()

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.ACTIVE
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )

        await repository.save_subscription(subscription_1)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


@test("expired subscription with overlapping payments")
async def _(db=db):
    repository = AssociationMembershipRepository()

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.ACTIVE
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2018, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2018, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )

        await repository.save_subscription(subscription_1)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.CANCELED


@test("subscription gets activated with overlapping payments")
async def _(db=db):
    repository = AssociationMembershipRepository()

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.CANCELED
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        await repository.save_subscription(subscription_1)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


@test("pending subscriptions are ignored")
async def _(db=db):
    repository = AssociationMembershipRepository()
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.PENDING
        )

        await repository.save_subscription(subscription_1)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.PENDING


@test("canceled subscriptions with no payments are left untouched")
async def _(db=db):
    repository = AssociationMembershipRepository()
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.CANCELED
        )

        await repository.save_subscription(subscription_1)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.CANCELED


@test("subscription with canceled payment gets canceled")
async def _(db=db):
    repository = AssociationMembershipRepository()

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = await SubscriptionFactory(
            user_id=1, status=SubscriptionStatus.ACTIVE
        )
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.CANCELED,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2022, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        await repository.save_subscription(subscription_1)

        await membership_check_status({})

        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.CANCELED
