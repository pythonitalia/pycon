from typing import Optional

from src.association_membership.domain.entities import Subscription, SubscriptionStatus


class FakeAssociationMembershipRepository:
    def __init__(self, subscriptions=None):
        self.SUBSCRIPTIONS_BY_USER_ID = {
            subscription.user_id: subscription for subscription in (subscriptions or [])
        }

    async def create_subscription(self, user):
        return Subscription(user_id=user.id, status=SubscriptionStatus.PENDING)

    async def get_user_subscription(self, user_id) -> Optional[Subscription]:
        return self.SUBSCRIPTIONS_BY_USER_ID.get(user_id, None)

    async def create_checkout_session(self, subscription: Subscription):
        return "cs_xxx"
