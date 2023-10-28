import pytest
import datetime
from datetime import timezone
from unittest.mock import call, patch

import time_machine
from association_membership.tests.factories import SubscriptionFactory

from association_membership.models import (
    Subscription,
)
from association_membership.enums import (
    PaymentStatus,
    SubscriptionStatus,
)
from association_membership.handlers.crons.membership_check_status import (
    membership_check_status,
)

pytestmark = pytest.mark.django_db


def test_no_expired_subscriptions():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
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

        subscription_2 = SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
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

        subscription_1.save()
        subscription_2.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE

        updated_subscription_2 = Subscription.objects.get(id=subscription_2.id)
        assert updated_subscription_2.status == SubscriptionStatus.ACTIVE


def test_one_expired_subscription():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
        )

        subscription_2 = SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
        subscription_2.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="AABBCC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        subscription_1.save()
        subscription_2.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.CANCELED

        updated_subscription_2 = Subscription.objects.get(id=subscription_2.id)
        assert updated_subscription_2.status == SubscriptionStatus.ACTIVE


def test_subscription_canceled_but_has_payment_for_this_range_is_activated():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.CANCELED)
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

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


def test_subscription_with_multiple_payments():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
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

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


def test_subscription_with_overlapping_payments():
    """
    Test that a subscription with overlapping payments is correctly handled
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
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

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


def test_expired_subscription_with_overlapping_payments():
    """
    Test that an expired subscription with overlapping payments is correctly handled
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.CANCELED)
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

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


def test_subscription_gets_activated_with_overlapping_payments():
    """
    Test that a subscription gets activated when it has overlapping payments
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.CANCELED)
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

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


def test_pending_subscriptions_are_ignored():
    """
    Pending subscriptions are ignored
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.PENDING)

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.PENDING


def test_canceled_subscriptions_with_no_payments_are_left_untouched():
    """
    Canceled subscriptions with no payments are left untouched
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.CANCELED)

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.CANCELED


def test_subscription_with_canceled_payment_gets_canceled():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
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

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.CANCELED


def test_subscription_with_overlapping_canceled_and_valid_payment_is_marked_active():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.CANCELED)
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

        subscription_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 11, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        subscription_1.save()

        membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE


def test_subscription_with_finished_and_new_payment():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        subscription_1 = SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
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
            payment_date=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2022, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )

        subscription_1.save()

    with time_machine.travel("2021-01-01 10:00:00", tick=False):
        with patch(
            "association_membership.handlers.crons.membership_check_status.logger"
        ) as logger_mock:
            membership_check_status({})

        updated_subscription_1 = Subscription.objects.get(id=subscription_1.id)
        assert updated_subscription_1.status == SubscriptionStatus.ACTIVE

    logger_mock.info.assert_has_calls(
        [
            call("Found subscriptions_to_cancel_count=%s subscriptions to cancel", 0),
            call("Found subscriptions_to_enable_count=%s subscriptions to activate", 0),
        ],
        any_order=True,
    )
