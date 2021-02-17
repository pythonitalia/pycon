from typing import List, Optional

from association.domain.entities.subscription_entities import (
    Subscription,
    SubscriptionRequest,
)
from association.domain.repositories.base import AbstractRepository
from sqlalchemy import select


class AssociationRepository(AbstractRepository):

    # READ
    async def get_subscription_request_by_session_id(
        self, session_id: str
    ) -> Optional[SubscriptionRequest]:
        query = select(SubscriptionRequest).where(
            SubscriptionRequest.stripe_session_id == session_id
        )
        subscription_request = (await self.session.execute(query)).scalar_one_or_none()
        return subscription_request

    async def get_subscription_request_by_subscription_id(
        self, subscription_id: str
    ) -> Optional[SubscriptionRequest]:
        query = select(SubscriptionRequest).where(
            SubscriptionRequest.stripe_subscription_id == subscription_id
        )
        subscription_request = (await self.session.execute(query)).scalar_one_or_none()
        return subscription_request

    async def get_subscription_by_stripe_id(
        self, stripe_id: str
    ) -> Optional[Subscription]:
        query = select(Subscription).where(Subscription.stripe_id == stripe_id)
        subscription = (await self.session.execute(query)).scalar_one_or_none()
        return subscription

    async def list_subscriptions_by_user_id(
        self, user_id: str
    ) -> List[Optional[Subscription]]:
        query = select(Subscription).where(Subscription.user_id == user_id)
        subscriptions = (await self.session.execute(query)).scalars()
        return subscriptions

    # WRITE
    async def register_subscription_request(
        self, subscription_request: SubscriptionRequest
    ) -> SubscriptionRequest:
        self.session.add(subscription_request)
        await self.session.flush()
        return subscription_request

    async def register_subscription(self, subscription: Subscription) -> Subscription:
        self.session.add(subscription)
        await self.session.flush()
        return subscription
