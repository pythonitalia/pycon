from datetime import datetime

from association.domain.repositories import AssociationRepository
from pydantic.main import BaseModel


class InvoicePaymentFailedInput(BaseModel):
    invoice_id: str
    subscription_id: str
    paid_at: datetime
    invoice_pdf: str


async def handle_invoice_payment_failed(
    invoice_input: InvoicePaymentFailedInput,
    association_repository: AssociationRepository,
):
    """
    We don't change the status of the subscription,
    but maybe we can notify staff users to contact directly the user
    Infact this procedure is automatic
    """
    # subscription = await association_repository.get_subscription_by_stripe_id(
    #     invoice_input.subscription_id
    # )
    # if subscription:
    #     if subscription.state == SubscriptionState.EXPIRED:
    #         notify_user()
    #     subscription.state = SubscriptionState.PAYMENT_FAILED
    #     await association_repository.save_subscription(subscription)
    #     await association_repository.commit()
    pass
