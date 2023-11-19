from datetime import datetime, timezone
import pytest

from association_membership.enums import MembershipStatus, PaymentStatus
from association_membership.tests.factories import MembershipFactory

pytestmark = pytest.mark.django_db


def test_move_membership_to_active():
    membership = MembershipFactory(status=MembershipStatus.PENDING)

    membership.mark_as_active()

    assert membership.status == MembershipStatus.ACTIVE
    assert membership.is_active


def test_move_membership_to_canceled():
    membership = MembershipFactory(status=MembershipStatus.PENDING)

    membership.mark_as_canceled()

    assert membership.status == MembershipStatus.CANCELED
    assert not membership.is_active


def test_add_stripe_payment():
    subscription = MembershipFactory(
        status=MembershipStatus.PENDING,
    )

    subscription.add_stripe_subscription_payment(
        total=1000,
        status=PaymentStatus.PAID,
        payment_date=datetime.fromtimestamp(1618062032, tz=timezone.utc),
        period_start=datetime.fromtimestamp(1618062032, tz=timezone.utc),
        period_end=datetime.fromtimestamp(1618062032, tz=timezone.utc),
        stripe_subscription_id="cs_xxx",
        stripe_invoice_id="iv_xx",
        invoice_pdf="https://pdfpdf",
    )

    assert subscription.payments.count() == 1
    assert subscription.payments.first().stripe_subscription_payments.exists()
    assert (
        subscription.payments.first()
        .stripe_subscription_payments.first()
        .stripe_subscription_id
        == "cs_xxx"
    )


def test_add_pretix_payment():
    subscription = MembershipFactory(
        status=MembershipStatus.PENDING,
    )

    subscription.add_pretix_payment(
        organizer="org",
        event="event",
        order_code="order_code",
        total=1000,
        status=PaymentStatus.PAID,
        payment_date=datetime.fromtimestamp(1618062032, tz=timezone.utc),
        period_start=datetime.fromtimestamp(1618062032, tz=timezone.utc),
        period_end=datetime.fromtimestamp(1618062032, tz=timezone.utc),
    )

    assert subscription.payments.count() == 1
    assert subscription.payments.first().pretix_payments.exists()
    assert (
        subscription.payments.first().pretix_payments.first().order_code == "order_code"
    )
    assert (
        subscription.payments.first().pretix_payments.first().event_organizer == "org"
    )
    assert subscription.payments.first().pretix_payments.first().event_id == "event"
