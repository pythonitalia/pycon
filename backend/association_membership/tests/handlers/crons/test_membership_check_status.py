import pytest
import datetime
from datetime import timezone
from unittest.mock import call, patch

import time_machine
from association_membership.tests.factories import MembershipFactory

from association_membership.models import (
    Membership,
)
from association_membership.enums import (
    PaymentStatus,
    MembershipStatus,
)
from association_membership.handlers.crons.membership_check_status import (
    membership_check_status,
)

pytestmark = pytest.mark.django_db


def test_no_expired_memberships():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.ACTIVE)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_2 = MembershipFactory(status=MembershipStatus.ACTIVE)
        membership_2.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="AABBCC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()
        membership_2.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.ACTIVE

        updated_membership_2 = Membership.objects.get(id=membership_2.id)
        assert updated_membership_2.status == MembershipStatus.ACTIVE


def test_one_expired_membership():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.ACTIVE)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 5, 5, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_2 = MembershipFactory(status=MembershipStatus.ACTIVE)
        membership_2.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="AABBCC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()
        membership_2.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.CANCELED

        updated_membership_2 = Membership.objects.get(id=membership_2.id)
        assert updated_membership_2.status == MembershipStatus.ACTIVE


def test_membership_canceled_but_has_payment_for_this_range_is_activated():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.CANCELED)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.ACTIVE


def test_membership_with_multiple_payments():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.ACTIVE)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.ACTIVE


def test_membership_with_overlapping_payments():
    """
    Test that a membership with overlapping payments is correctly handled
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.ACTIVE)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.ACTIVE


def test_expired_membership_with_overlapping_payments():
    """
    Test that an expired membership with overlapping payments is correctly handled
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.CANCELED)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.ACTIVE


def test_membership_gets_activated_with_overlapping_payments():
    """
    Test that a membership gets activated when it has overlapping payments
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.CANCELED)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.ACTIVE


def test_pending_memberships_are_ignored():
    """
    Pending memberships are ignored
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.PENDING)

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.PENDING


def test_canceled_memberships_with_no_payments_are_left_untouched():
    """
    Canceled memberships with no payments are left untouched
    """

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.CANCELED)

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.CANCELED


def test_membership_with_canceled_payment_gets_canceled():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.ACTIVE)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.CANCELED,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2022, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.CANCELED


def test_membership_with_overlapping_canceled_and_valid_payment_is_marked_active():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.CANCELED)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.CANCELED,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2022, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2019, 10, 10, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2020, 11, 10, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()

        membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.ACTIVE


def test_membership_with_finished_and_new_payment():
    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        membership_1 = MembershipFactory(status=MembershipStatus.ACTIVE)
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="ABCABCABC",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2020, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )
        membership_1.add_pretix_payment(
            organizer="python-italia",
            event="pycon-demo",
            order_code="XXYYZZ",
            total=1000,
            status=PaymentStatus.PAID,
            payment_date=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_start=datetime.datetime(2021, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
            period_end=datetime.datetime(2022, 1, 1, 1, 4, 43, tzinfo=timezone.utc),
        )

        membership_1.save()

    with time_machine.travel("2021-01-01 10:00:00", tick=False):
        with patch(
            "association_membership.handlers.crons.membership_check_status.logger"
        ) as logger_mock:
            membership_check_status({})

        updated_membership_1 = Membership.objects.get(id=membership_1.id)
        assert updated_membership_1.status == MembershipStatus.ACTIVE

    logger_mock.info.assert_has_calls(
        [
            call("Found subscriptions_to_cancel_count=%s subscriptions to cancel", 0),
            call("Found subscriptions_to_enable_count=%s subscriptions to activate", 0),
        ],
        any_order=True,
    )
