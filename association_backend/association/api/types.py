from __future__ import annotations

from datetime import datetime

import strawberry
from association.domain import entities


@strawberry.type
class Subscription:
    user_id: str
    creation_date: datetime
    payment_date: datetime
    stripe_id: str
    stripe_customer_id: str
    state: str
    stripe_session_id: str

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
        )
