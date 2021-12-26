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
from src.webhooks.handlers.crons.membership_check_expiration import (
    membership_check_expiration,
)


@test("with no expired subscriptions")
async def _(db=db):
    repository = AssociationMembershipRepository()
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(
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

        subscription_2 = SubscriptionFactory(
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

        await membership_check_expiration({})

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
        subscription_1 = SubscriptionFactory(
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

        subscription_2 = SubscriptionFactory(
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

        await membership_check_expiration({})

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


@test("expired subscriptions are not touched")
async def _(db=db):
    repository = AssociationMembershipRepository()

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(
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

        subscription_2 = SubscriptionFactory(
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

        await membership_check_expiration({})

        # subscription_1 technically should be active since has a payment
        # but this cron only handles ACTIVE -> CANCELED
        # so it is left untouched
        updated_subscription_1 = await Subscription.objects.get_or_none(
            id=subscription_1.id
        )
        assert updated_subscription_1.status == SubscriptionStatus.CANCELED

        updated_subscription_2 = await Subscription.objects.get_or_none(
            id=subscription_2.id
        )
        assert updated_subscription_2.status == SubscriptionStatus.CANCELED
