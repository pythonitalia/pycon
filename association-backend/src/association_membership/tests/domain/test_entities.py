from datetime import datetime, timezone

from ward import test

from src.association_membership.domain.entities import (
    PaymentStatus,
    Subscription,
    SubscriptionStatus,
)


@test("change subscription status to active")
async def _():
    subscription = Subscription(
        id=1,
        user_id=1,
        status=SubscriptionStatus.PENDING,
    )

    subscription.mark_as_active()

    assert subscription.is_active
    assert subscription.status == SubscriptionStatus.ACTIVE


@test("change subscription status to canceled")
async def _():
    subscription = Subscription(
        id=1,
        status=SubscriptionStatus.PENDING,
    )

    subscription.mark_as_canceled()

    assert not subscription.is_active
    assert subscription.status == SubscriptionStatus.CANCELED


@test("add stripe subscription payment to subscription")
async def _():
    subscription = Subscription(
        id=1,
        status=SubscriptionStatus.PENDING,
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

    assert len(subscription._add_stripe_subscription_payment) > 0
    assert subscription._add_stripe_subscription_payment[0].stripe_subscription_id == "cs_xxx"
