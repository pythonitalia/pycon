import logging
from datetime import datetime, timezone

from association_membership.domain.entities import InvoiceStatus, SubscriptionInvoice
from association_membership.domain.repository import AssociationMembershipRepository
from customers.domain.repository import CustomersRepository

logger = logging.getLogger(__name__)


async def handle_invoice_paid(event):
    invoice = event.data.object
    stripe_customer_id = invoice.customer
    stripe_subscription_id = invoice.subscription

    customers_repository = CustomersRepository()
    customer = await customers_repository.get_for_stripe_customer_id(stripe_customer_id)

    if not customer:
        logger.error(
            "Unable to process stripe event invoice paid because stripe_customer_id=%s"
            " doesn't have an associated Customer locally",
            stripe_customer_id,
        )
        return

    membership_repository = AssociationMembershipRepository()
    subscription = await membership_repository.get_or_create_subscription(
        customer=customer, stripe_subscription_id=stripe_subscription_id
    )

    # Take the first item they purchased
    # users can only buy the subscription
    # so the lines will always be 1
    assert len(invoice.lines.data) == 1

    invoice_period = invoice.lines.data[0].period
    subscription.add_invoice(
        SubscriptionInvoice(
            status=InvoiceStatus(invoice.status),
            subscription=subscription,
            payment_date=datetime.fromtimestamp(
                invoice.status_transitions.paid_at, tz=timezone.utc
            ),
            period_start=datetime.fromtimestamp(invoice_period.start, tz=timezone.utc),
            period_end=datetime.fromtimestamp(invoice_period.end, tz=timezone.utc),
            stripe_invoice_id=invoice.id,
            invoice_pdf=invoice.invoice_pdf,
        )
    )
    subscription.mark_as_active()
    await membership_repository.save_subscription(subscription)


async def handle_customer_subscription_deleted(event):
    stripe_subscription = event.data.object
    membership_repository = AssociationMembershipRepository()
    subscription = await membership_repository.get_by_stripe_id(stripe_subscription.id)

    if not subscription:
        logger.error(
            "Received subscription canceled for subscription %s"
            " but no subscription with this stripe id exists in our"
            " database!",
            stripe_subscription.id,
        )
        return

    subscription.mark_as_canceled()
    await membership_repository.save_subscription(subscription)
    logger.info(
        "Successfully marked local subscription_id=%s"
        " as canceled from stripe event for stripe_subscription_id=%s",
        subscription.id,
        stripe_subscription.id,
    )


HANDLERS = {
    "customer.subscription.deleted": handle_customer_subscription_deleted,
    "invoice.paid": handle_invoice_paid,
}
