from __future__ import annotations

import logging
from datetime import datetime

from association.domain.entities.subscription_entities import (
    Subscription,
    SubscriptionState,
)
from association.domain.repositories.association_repository import AssociationRepository
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SubscriptionDraftInput(BaseModel):
    user_id: str
    session_id: str
    customer_id: str


async def create_draft_subscription(
    data: SubscriptionDraftInput, association_repository: AssociationRepository
):
    subscription = Subscription(
        user_id=data.user_id,
        stripe_session_id=data.session_id,
        stripe_customer_id=data.customer_id,
        creation_date=datetime.now(),
        state=SubscriptionState.PENDING,
    )
    await association_repository.save_subscription(subscription)
    await association_repository.commit()
    return subscription
