from __future__ import annotations

from datetime import datetime

import strawberry
from association.domain import entities


@strawberry.type
class Subscription:
    user_id: str
    payment_date: datetime
    stripe_id: str
    stripe_customer_id: str

    @classmethod
    def from_domain(cls, entity: entities.Subscription) -> Subscription:
        return cls(
            user_id=entity.user_id,
            payment_date=entity.payment_date,
            stripe_id=entity.stripe_id,
            stripe_customer_id=entity.stripe_customer_id,
        )


@strawberry.type
class SubscriptionRequest:
    user_id: str
    request_date: datetime
    stripe_session_id: str
    stripe_customer_id: str

    @classmethod
    def from_domain(cls, entity: entities.SubscriptionRequest) -> SubscriptionRequest:
        return cls(
            user_id=entity.user_id,
            stripe_customer_id=entity.stripe_customer_id,
            request_date=entity.request_date,
            stripe_session_id=entity.stripe_session_id,
        )
