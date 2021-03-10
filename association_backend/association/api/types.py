from __future__ import annotations

from datetime import datetime
from typing import Optional

import strawberry

from association.domain import entities


@strawberry.type
class SubscriptionResponse:
    user_id: int
    creation_date: datetime
    state: str
    stripe_session_id: str
    due_date: Optional[datetime]
    stripe_id: Optional[str]
    stripe_customer_id: Optional[str]
    expiration_date: Optional[datetime]

    @classmethod
    def from_domain(cls, entity: entities.Subscription) -> SubscriptionResponse:
        return cls(
            user_id=entity.user_id,
            creation_date=entity.creation_date,
            due_date=entity.due_date,
            stripe_id=entity.stripe_id,
            stripe_customer_id=entity.stripe_customer_id,
            state=entity.state,
            stripe_session_id=entity.stripe_session_id,
            expiration_date=entity.expiration_date,
        )
