import pytest
from datetime import datetime, timezone

import time_machine
from stripe import util

from association_membership.enums import (
    PaymentStatus,
    SubscriptionStatus,
)
from association_membership.models import (
    Subscription,
)
from association_membership.tests.factories import (
    StripeCustomerFactory,
    SubscriptionFactory,
)
from association_membership.exceptions import NoCustomerFoundForEvent
from association_membership.handlers.stripe.handle_invoice_paid import (
    handle_invoice_paid,
)
from association_membership.tests.handlers.stripe.payloads import (
    INVOICE_PAID_PAYLOAD,
    RAW_INVOICE_PAID_PAYLOAD,
)
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_receive_a_paid_stripe_subscription_invoice():
    user = UserFactory(email="stripe@example.org")
    subscription = SubscriptionFactory(user=user)
    StripeCustomerFactory(user=user, stripe_customer_id="cus_customer_id")

    with time_machine.travel("2022-02-10 12:00:00", tick=False):
        handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    subscription = Subscription.objects.get(user=user)

    assert subscription.status == SubscriptionStatus.ACTIVE

    payment = subscription.payments.first()
    assert payment.status == PaymentStatus.PAID
    assert payment.total == 1000
    assert payment.subscription.id == subscription.id
    assert payment.payment_date == datetime.fromtimestamp(1618062032, tz=timezone.utc)
    assert payment.period_start == datetime.fromtimestamp(1618062031, tz=timezone.utc)
    assert payment.period_end == datetime.fromtimestamp(1649598031, tz=timezone.utc)

    stripe_subscription_payment = payment.stripe_subscription_payments.first()
    assert stripe_subscription_payment.stripe_subscription_id == "sub_subscription_id"
    assert (
        stripe_subscription_payment.stripe_invoice_id == "in_1Ieh35AQv52awOkHrNk0JBjD"
    )
    assert (
        stripe_subscription_payment.invoice_pdf
        == "https://pay.stripe.com/invoice/acct_1AEbpzAQv52awOkH/invst_JHFYBOjnsmDH6yxnhbD2jeX09nN1QUC/pdf"
    )


def test_receive_same_paid_invoice_twice_does_not_record_payment_twice():
    user = UserFactory(email="stripe@example.org")
    subscription = SubscriptionFactory(user_id=user.id)
    StripeCustomerFactory(user_id=user.id, stripe_customer_id="cus_customer_id")

    with time_machine.travel("2022-02-10 12:00:00", tick=False):
        handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    subscription = Subscription.objects.get(user_id=user.id)
    assert subscription.status == SubscriptionStatus.ACTIVE
    assert subscription.payments.count() == 1

    handle_invoice_paid(INVOICE_PAID_PAYLOAD)

    subscription = Subscription.objects.get(user_id=user.id)
    assert subscription.status == SubscriptionStatus.ACTIVE
    assert subscription.payments.count() == 1


def test_receive_a_paid_invoice_for_the_past_doesnt_mark_it_as_active():
    user = UserFactory(email="stripe@example.org")
    subscription = SubscriptionFactory(user_id=user.id)
    StripeCustomerFactory(user_id=user.id, stripe_customer_id="cus_customer_id")

    with time_machine.travel("2021-10-10 12:00:00", tick=False):
        handle_invoice_paid(
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
                                            # Mon Dec 14 2020 20:54:32 GMT+0000
                                            "end": 1607979272,
                                            # Sat Dec 14 2019 20:54:32 GMT+0000
                                            "start": 1576356872,
                                        },
                                    }
                                ],
                            },
                        },
                    },
                }
            )
        )

    subscription = Subscription.objects.get(user_id=user.id)
    assert subscription.status == SubscriptionStatus.PENDING
    assert subscription.payments.count() == 1


def test_receiving_a_paid_invoice_for_a_customer_without_subscription_throws_an_error():
    with pytest.raises(NoCustomerFoundForEvent):
        handle_invoice_paid(INVOICE_PAID_PAYLOAD)
