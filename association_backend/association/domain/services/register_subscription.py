from __future__ import annotations

import logging
from datetime import datetime

from association.domain.entities.subscription_entities import Subscription
from association.domain.repositories.association_repository import AssociationRepository
from association.domain.services.exceptions import SubscriptionNotCreated
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SubscriptionInputModel(BaseModel):
    subscription_id: str


async def register_subscription(
    data: SubscriptionInputModel, association_repository: AssociationRepository
):
    subscription_request = await association_repository.get_subscription_request_by_subscription_id(
        data.subscription_id
    )
    if subscription_request:
        subscription = Subscription(
            user_id=subscription_request.user_id,
            stripe_id=data.subscription_id,
            payment_date=datetime.now(),
            stripe_customer_id=subscription_request.stripe_customer_id,
        )
        subscription = await association_repository.register_subscription(subscription)
        await association_repository.commit()
        return subscription
    else:
        msg = (
            f"No Subscription Request found with subscription_id:{data.subscription_id}"
        )
        logger.warning(msg)
        raise SubscriptionNotCreated(msg)
