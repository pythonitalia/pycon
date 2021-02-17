from __future__ import annotations

import logging

from association.domain.repositories.association_repository import AssociationRepository
from association.domain.services.exceptions import SubscriptionRequestNotUpdated
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SubscriptionRequestUpdateInput(BaseModel):
    session_id: str
    customer_id: str
    subscription_id: str


async def update_subscription_request(
    data: SubscriptionRequestUpdateInput, association_repository: AssociationRepository
):
    subscription_request = await association_repository.get_subscription_request_by_session_id(
        data.session_id
    )
    if subscription_request:
        subscription_request.stripe_customer_id = data.customer_id
        subscription_request.stripe_subscription_id = data.subscription_id
        await association_repository.register_subscription_request(subscription_request)
        await association_repository.commit()
        return subscription_request
    else:
        msg = f"No Subscription Request found with session_id:{data.session_id}"
        logger.warning(msg)
        raise SubscriptionRequestNotUpdated(msg)
