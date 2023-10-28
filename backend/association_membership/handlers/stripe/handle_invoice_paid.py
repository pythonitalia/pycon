from django.db import transaction
import logging
from datetime import datetime, timezone
from association_membership.models import Payment, StripeCustomer, Subscription
from association_membership.enums import PaymentStatus
from association_membership.exceptions import NoCustomerFoundForEvent

logger = logging.getLogger(__name__)


def handle_invoice_paid(event):
    invoice = event.data.object
    stripe_customer_id = invoice.customer
    stripe_subscription_id = invoice.subscription

    # Take the first item they purchased
    # users can only buy the subscription
    # so the lines will always be 1
    # If we change and allow people to buy
    # multiple this we need to update this
    assert (
        len(invoice.lines.data) == 1
    ), f"event_id={event.id} has more items than excepted"
    assert (
        invoice.status == "paid"
    ), f"event_id={event.id} has invoice_status={invoice.status}"

    stripe_customer = StripeCustomer.objects.filter(
        stripe_customer_id=stripe_customer_id
    ).first()

    subscription = (
        Subscription.objects.filter(user_id=stripe_customer.user_id).first()
        if stripe_customer
        else None
    )

    if not subscription or not stripe_customer:
        logger.error(
            "Unable to process stripe event_id=%s invoice paid "
            "because stripe_customer_id=%s "
            "doesn't have an associated Customer locally or a subscription",
            event.id,
            stripe_customer_id,
        )
        raise NoCustomerFoundForEvent()

    if Payment.is_payment_already_processed(invoice.id):
        logger.info(
            "Ignoring event_id=%s from Stripe because we already processed "
            "the payment of invoice_id=%s",
            event.id,
            invoice.id,
        )
        return

    invoice_period = invoice.lines.data[0].period

    period_start = datetime.fromtimestamp(invoice_period.start, tz=timezone.utc)
    period_end = datetime.fromtimestamp(invoice_period.end, tz=timezone.utc)
    now = datetime.now(timezone.utc)

    with transaction.atomic():
        subscription.add_stripe_subscription_payment(
            total=invoice.total,
            status=PaymentStatus.PAID,
            payment_date=datetime.fromtimestamp(
                invoice.status_transitions.paid_at, tz=timezone.utc
            ),
            period_start=period_start,
            period_end=period_end,
            stripe_subscription_id=stripe_subscription_id,
            stripe_invoice_id=invoice.id,
            invoice_pdf=invoice.invoice_pdf,
        )

        # If the payment we just received is for the current
        # period, we mark the subscription as active
        if period_start <= now <= period_end:
            subscription.mark_as_active()

        subscription.save(update_fields=["status"])
