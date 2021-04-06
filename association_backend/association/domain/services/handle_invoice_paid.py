import logging
from datetime import datetime

from pydantic import BaseModel

from association.domain.entities.subscriptions import SubscriptionPayment
from association.domain.exceptions import SubscriptionNotFound
from association.domain.repositories.association_repository import AssociationRepository

logger = logging.getLogger(__name__)


class InvoicePaidInput(BaseModel):
    invoice_id: str
    subscription_id: str
    paid_at: datetime
    invoice_pdf: str


async def handle_invoice_paid(
    invoice_input: InvoicePaidInput, association_repository: AssociationRepository
):
    subscription = (
        await association_repository.get_subscription_by_stripe_subscription_id(
            invoice_input.subscription_id
        )
    )
    if subscription:
        payment = await association_repository.get_payment_by_stripe_invoice_id(
            invoice_input.invoice_id
        )
        if not payment:
            payment = SubscriptionPayment(
                payment_date=invoice_input.paid_at,
                subscription=subscription,
                stripe_invoice_id=invoice_input.invoice_id,
                invoice_pdf=invoice_input.invoice_pdf,
            )
            await association_repository.save_payment(payment)
            await association_repository.commit()
            return subscription
        else:
            logger.debug("Payment already registered")
    else:
        msg = f"No Subscription found with subscription_id:{invoice_input.subscription_id}"
        logger.warning(msg)
        raise SubscriptionNotFound(msg)
