from datetime import datetime, timedelta, timezone

from ward import raises, test

from association.tests.session import db
from association_membership.domain.entities import (
    InvoiceStatus,
    Subscription,
    SubscriptionStatus,
)
from association_membership.tests.factories import (
    SubscriptionFactory,
    SubscriptionInvoiceFactory,
)
from customers.tests.factories import CustomerFactory
from webhooks.exceptions import NoCustomerFoundForEvent, NoSubscriptionFoundForEvent
from webhooks.handlers import handle_customer_subscription_deleted, handle_invoice_paid
from webhooks.tests.payloads import (
    CUSTOMER_SUBSCRIPTION_DELETED_PAYLOAD,
    INVOICE_PAID_PAYLOAD,
)


@test("invoice paid with users without existing subscription")
async def _(db=db):
    customer = await CustomerFactory(stripe_customer_id="cus_customer_id")

    await handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    subscription = await Subscription.objects.select_related("invoices").get(
        stripe_subscription_id="sub_subscription_id"
    )

    assert subscription.status == SubscriptionStatus.ACTIVE
    assert subscription.customer.id == customer.id

    invoice = subscription.invoices[0]
    assert invoice.status == InvoiceStatus.PAID
    assert invoice.subscription.id == subscription.id
    assert invoice.payment_date == datetime.fromtimestamp(1618062032, tz=timezone.utc)
    assert invoice.period_start == datetime.fromtimestamp(1618062031, tz=timezone.utc)
    assert invoice.period_end == datetime.fromtimestamp(1649598031, tz=timezone.utc)
    assert invoice.stripe_invoice_id == "in_1Ieh35AQv52awOkHrNk0JBjD"
    assert (
        invoice.invoice_pdf
        == "https://pay.stripe.com/invoice/acct_1AEbpzAQv52awOkH/invst_JHFYBOjnsmDH6yxnhbD2jeX09nN1QUC/pdf"
    )


@test("invoice paid with users with existing subscription")
async def _(db=db):
    customer = await CustomerFactory(stripe_customer_id="cus_customer_id")

    subscription = await SubscriptionFactory(
        customer=customer, stripe_subscription_id="sub_subscription_id"
    )

    now = datetime.now(timezone.utc)
    await SubscriptionInvoiceFactory(
        subscription=subscription,
        payment_date=now - timedelta(days=300),
        period_start=now - timedelta(days=300),
        period_end=now - timedelta(days=250),
        status=InvoiceStatus.PAID,
    )

    await handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    refreshed_subscription = await Subscription.objects.select_related("invoices").get(
        stripe_subscription_id="sub_subscription_id"
    )

    assert refreshed_subscription.status == SubscriptionStatus.ACTIVE

    assert len(refreshed_subscription.invoices) == 2

    invoices = sorted(
        refreshed_subscription.invoices, key=lambda invoice: invoice.payment_date
    )

    invoice = invoices[1]
    assert invoice.status == InvoiceStatus.PAID
    assert invoice.subscription.id == refreshed_subscription.id
    assert invoice.payment_date == datetime.fromtimestamp(1618062032, tz=timezone.utc)
    assert invoice.period_start == datetime.fromtimestamp(1618062031, tz=timezone.utc)
    assert invoice.period_end == datetime.fromtimestamp(1649598031, tz=timezone.utc)
    assert invoice.stripe_invoice_id == "in_1Ieh35AQv52awOkHrNk0JBjD"
    assert (
        invoice.invoice_pdf
        == "https://pay.stripe.com/invoice/acct_1AEbpzAQv52awOkH/invst_JHFYBOjnsmDH6yxnhbD2jeX09nN1QUC/pdf"
    )


@test("invoice paid to user without customer")
async def _(db=db):
    with raises(NoCustomerFoundForEvent):
        await handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    assert (
        await Subscription.objects.select_related("invoices")
        .filter(stripe_subscription_id="sub_subscription_id")
        .exists()
        is False
    )


@test("subscription deleted but doesnt exist locally")
async def _(db=db):
    with raises(NoSubscriptionFoundForEvent):
        await handle_customer_subscription_deleted(
            CUSTOMER_SUBSCRIPTION_DELETED_PAYLOAD
        )


@test("subscription deleted")
async def _(db=db):
    subscription = await SubscriptionFactory(
        customer__stripe_customer_id="cus_customer_id",
        stripe_subscription_id="sub_subscription_id",
    )

    await handle_customer_subscription_deleted(CUSTOMER_SUBSCRIPTION_DELETED_PAYLOAD)

    refreshed_subscription = await Subscription.objects.get(id=subscription.id)

    assert refreshed_subscription.status == SubscriptionStatus.CANCELED


@test("subscription deleted for an already canceled subscription")
async def _(db=db):
    subscription = await SubscriptionFactory(
        customer__stripe_customer_id="cus_customer_id",
        stripe_subscription_id="sub_subscription_id",
    )

    await handle_customer_subscription_deleted(CUSTOMER_SUBSCRIPTION_DELETED_PAYLOAD)

    refreshed_subscription = await Subscription.objects.get(id=subscription.id)

    assert refreshed_subscription.status == SubscriptionStatus.CANCELED

    await handle_customer_subscription_deleted(CUSTOMER_SUBSCRIPTION_DELETED_PAYLOAD)

    refreshed_subscription = await Subscription.objects.get(id=subscription.id)

    assert refreshed_subscription.status == SubscriptionStatus.CANCELED
