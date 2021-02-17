from __future__ import annotations

import logging
from datetime import datetime

from association.domain.entities.subscription_entities import SubscriptionRequest
from association.domain.repositories.association_repository import AssociationRepository
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SubscriptionRequestInput(BaseModel):
    user_id: str
    session_id: str
    customer_id: str


async def create_subscription_request(
    data: SubscriptionRequestInput, association_repository: AssociationRepository
):
    subscription_request = SubscriptionRequest(
        user_id=data.user_id,
        stripe_session_id=data.session_id,
        stripe_customer_id=data.customer_id,
        request_date=datetime.now(),
    )
    await association_repository.register_subscription_request(subscription_request)
    await association_repository.commit()
    return subscription_request
