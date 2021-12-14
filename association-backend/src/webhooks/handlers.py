import logging
from datetime import datetime, timezone

from src.association_membership.domain.entities import PaymentStatus
from src.association_membership.domain.repository import AssociationMembershipRepository
from src.webhooks.exceptions import NoCustomerFoundForEvent

logger = logging.getLogger(__name__)


async def handle_invoice_paid(event):
    invoice = event.data.object
    stripe_customer_id = invoice.customer
    stripe_subscription_id = invoice.subscription

    # Take the first item they purchased
    # users can only buy the subscription
    # so the lines will always be 1
    # If we change and allow people to buy
    # multiple this, we need to fix this
    assert len(invoice.lines.data) == 1
    assert invoice.status == "paid"

    membership_repository = AssociationMembershipRepository()
    subscription = await membership_repository.get_subscription_from_stripe_customer(
        stripe_customer_id
    )

    if not subscription:
        logger.error(
            "Unable to process stripe event invoice paid because stripe_customer_id=%s"
            " doesn't have an associated Customer locally or a subscription",
            stripe_customer_id,
        )
        raise NoCustomerFoundForEvent()

    invoice_period = invoice.lines.data[0].period

    period_start = datetime.fromtimestamp(invoice_period.start, tz=timezone.utc)
    period_end = datetime.fromtimestamp(invoice_period.end, tz=timezone.utc)
    now = datetime.now(timezone.utc)

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
    await membership_repository.save_subscription(subscription)


HANDLERS = {
    "invoice.paid": handle_invoice_paid,
}
