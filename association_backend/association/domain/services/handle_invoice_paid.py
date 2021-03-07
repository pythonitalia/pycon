import logging
from datetime import datetime

from association.domain.entities.subscription_entities import (
    SubscriptionPayment,
    SubscriptionState,
)
from association.domain.exceptions import SubscriptionNotFound
from association.domain.repositories.association_repository import AssociationRepository
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class InvoicePaidInput(BaseModel):
    invoice_id: str
    subscription_id: str
    paid_at: datetime
    invoice_pdf: str


async def handle_invoice_paid(
    invoice_input: InvoicePaidInput, association_repository: AssociationRepository
):
    subscription = await association_repository.get_subscription_by_stripe_id(
        invoice_input.subscription_id
    )
    if subscription:
        payment = SubscriptionPayment(
            payment_date=invoice_input.paid_at,
            subscription=subscription,
            invoice_id=invoice_input.invoice_id,
            invoice_pdf=invoice_input.invoice_pdf,
        )
        await association_repository.save_payment(payment)
        subscription.state = SubscriptionState.ACTIVE
        await association_repository.save_subscription(subscription)
        await association_repository.commit()
    else:
        msg = f"No Subscription found with subscription_id:{invoice_input.subscription_id}"
        logger.warning(msg)
        raise SubscriptionNotFound(msg)
