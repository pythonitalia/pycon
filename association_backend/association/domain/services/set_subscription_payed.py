from __future__ import annotations

import logging
from datetime import datetime

from association.domain.entities.subscription_entities import SubscriptionState
from association.domain.repositories.association_repository import AssociationRepository
from association.domain.services.exceptions import SubscriptionNotCreated
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SubscriptionInputModel(BaseModel):
    subscription_id: str


async def set_subscription_payed(
    data: SubscriptionInputModel, association_repository: AssociationRepository
):
    subscription = await association_repository.get_subscription_by_stripe_id(
        data.subscription_id
    )
    if subscription:
        subscription.payment_date = datetime.now()  # TODO Take it from Stripe
        subscription.state = SubscriptionState.ACTIVE
        subscription = await association_repository.save_subscription(subscription)
        await association_repository.commit()
        return subscription
    else:
        msg = (
            f"No Subscription Request found with subscription_id:{data.subscription_id}"
        )
        logger.warning(msg)
        raise SubscriptionNotCreated(msg)
