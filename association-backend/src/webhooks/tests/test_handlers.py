from datetime import datetime, timezone

from stripe import util
from ward import raises, test

from src.association.tests.session import db
from src.association_membership.domain.entities import (
    PaymentStatus,
    Subscription,
    SubscriptionStatus,
)
from src.association_membership.tests.factories import (
    StripeCustomerFactory,
    SubscriptionFactory,
)
from src.webhooks.exceptions import NoCustomerFoundForEvent
from src.webhooks.handlers import handle_invoice_paid
from src.webhooks.tests.payloads import INVOICE_PAID_PAYLOAD, RAW_INVOICE_PAID_PAYLOAD


@test("receive a paid stripe subscription invoice")
async def _(db=db):
    subscription = await SubscriptionFactory(user_id=1)
    await StripeCustomerFactory(user_id=1, stripe_customer_id="cus_customer_id")
    await handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    subscription = await Subscription.objects.select_related(
        ["payments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)

    assert subscription.status == SubscriptionStatus.ACTIVE

    payment = subscription.payments[0]
    assert payment.status == PaymentStatus.PAID
    assert payment.total == 1000
    assert payment.subscription.id == subscription.id
    assert payment.payment_date == datetime.fromtimestamp(1618062032, tz=timezone.utc)
    assert payment.period_start == datetime.fromtimestamp(1618062031, tz=timezone.utc)
    assert payment.period_end == datetime.fromtimestamp(1649598031, tz=timezone.utc)

    stripe_subscription_payment = payment.stripesubscriptionpayments[0]
    assert stripe_subscription_payment.stripe_subscription_id == "sub_subscription_id"
    assert (
        stripe_subscription_payment.stripe_invoice_id == "in_1Ieh35AQv52awOkHrNk0JBjD"
    )
    assert (
        stripe_subscription_payment.invoice_pdf
        == "https://pay.stripe.com/invoice/acct_1AEbpzAQv52awOkH/invst_JHFYBOjnsmDH6yxnhbD2jeX09nN1QUC/pdf"
    )


@test("receive the same paid invoice twice doesn't record the payment twice")
async def _(db=db):
    subscription = await SubscriptionFactory(user_id=1)
    await StripeCustomerFactory(user_id=1, stripe_customer_id="cus_customer_id")

    await handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    subscription = await Subscription.objects.select_related(
        ["payments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)
    assert subscription.status == SubscriptionStatus.ACTIVE
    assert len(subscription.payments) == 1

    await handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    subscription = await Subscription.objects.select_related(
        ["payments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)
    assert subscription.status == SubscriptionStatus.ACTIVE
    assert len(subscription.payments) == 1


@test("receive a paid invoice for the past doesn't mark it as active")
async def _(db=db):
    subscription = await SubscriptionFactory(user_id=1)
    await StripeCustomerFactory(user_id=1, stripe_customer_id="cus_customer_id")

    await handle_invoice_paid(
        util.convert_to_stripe_object(
            {
                **RAW_INVOICE_PAID_PAYLOAD,
                "data": {
                    **RAW_INVOICE_PAID_PAYLOAD["data"],
                    "object": {
                        **RAW_INVOICE_PAID_PAYLOAD["data"]["object"],
                        "lines": {
                            "data": [
                                {
                                    **RAW_INVOICE_PAID_PAYLOAD["data"]["object"][
                                        "lines"
                                    ]["data"][0],
                                    "period": {
                                        "end": 1607979272,  # Mon Dec 14 2020 20:54:32 GMT+0000
                                        "start": 1576356872,  # Sat Dec 14 2019 20:54:32 GMT+0000
                                    },
                                }
                            ],
                        },
                    },
                },
            }
        )
    )

    subscription = await Subscription.objects.select_related(
        ["payments", "payments__stripesubscriptionpayments"]
    ).get(user_id=1)
    assert subscription.status == SubscriptionStatus.PENDING
    assert len(subscription.payments) == 1


@test("receiving a paid invoice for a customer without subscription throws an error")
async def _(db=db):
    with raises(NoCustomerFoundForEvent):
        await handle_invoice_paid(INVOICE_PAID_PAYLOAD)
