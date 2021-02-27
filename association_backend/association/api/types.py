from __future__ import annotations

from datetime import datetime
from typing import Optional

import strawberry
from association.domain import entities


@strawberry.type
class Subscription:
    user_id: str
    creation_date: datetime
    state: str
    stripe_session_id: str
    payment_date: Optional[datetime]
    stripe_id: Optional[str]
    stripe_customer_id: Optional[str]
    expiration_date: Optional[datetime]

    @classmethod
    def from_domain(cls, entity: entities.Subscription) -> Subscription:
        return cls(
            user_id=entity.user_id,
            creation_date=entity.creation_date,
            payment_date=entity.payment_date,
            stripe_id=entity.stripe_id,
            stripe_customer_id=entity.stripe_customer_id,
            state=entity.state,
            stripe_session_id=entity.stripe_session_id,
            expiration_date=entity.expiration_date,
        )
