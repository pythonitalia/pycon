import logging

from pydantic import BaseModel

from association.domain.exceptions import SubscriptionNotUpdated
from association.domain.repositories.association_repository import AssociationRepository

logger = logging.getLogger(__name__)


class SubscriptionUpdateInput(BaseModel):
    session_id: str
    customer_id: str
    subscription_id: str


async def handle_checkout_session_completed(
    data: SubscriptionUpdateInput, association_repository: AssociationRepository
):
    subscription = await association_repository.get_subscription_by_session_id(
        data.session_id
    )
    if subscription:
        subscription.stripe_customer_id = data.customer_id
        subscription.stripe_id = data.subscription_id
        subscription = await association_repository.save_subscription(subscription)
        await association_repository.commit()
        return subscription
    else:
        msg = f"No Subscription Request found with session_id:{data.session_id}"
        logger.warning(msg)
        raise SubscriptionNotUpdated(msg)
