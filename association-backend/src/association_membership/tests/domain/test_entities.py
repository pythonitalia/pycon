from datetime import datetime, timedelta, timezone

from ward import fixture, test

from src.association_membership.domain.entities import (
    InvoiceStatus,
    Subscription,
    SubscriptionInvoice,
    SubscriptionStatus,
)
from src.customers.domain.entities import Customer


@fixture
def fake_customer():
    return Customer(id=1, user_id=1, stripe_customer_id="cus_11")


@test("change subscription status to active")
async def _(fake_customer=fake_customer):
    subscription = Subscription(
        id=1,
        stripe_subscription_id="sub_1",
        customer=fake_customer,
        status=SubscriptionStatus.PENDING,
    )

    subscription.mark_as_active()

    assert subscription.is_active
    assert subscription.status == SubscriptionStatus.ACTIVE


@test("change subscription status to canceled")
async def _(fake_customer=fake_customer):
    subscription = Subscription(
        id=1,
        stripe_subscription_id="sub_1",
        customer=fake_customer,
        status=SubscriptionStatus.PENDING,
    )

    subscription.mark_as_canceled()

    assert not subscription.is_active
    assert subscription.status == SubscriptionStatus.CANCELED


@test("add invoice to subscription")
async def _(fake_customer=fake_customer):
    subscription = Subscription(
        id=1,
        stripe_subscription_id="sub_1",
        customer=fake_customer,
        status=SubscriptionStatus.PENDING,
    )

    invoice = SubscriptionInvoice(
        status=InvoiceStatus.OPEN,
        subscription=subscription,
        payment_date=datetime.now(timezone.utc),
        period_start=datetime.now(timezone.utc),
        period_end=datetime.now(timezone.utc) + timedelta(days=30),
        stripe_invoice_id="ivv_invoice",
        invoice_pdf="https://invoice.stripe/invoice/",
    )
    subscription.add_invoice(invoice)

    assert subscription._add_invoice == [invoice]
