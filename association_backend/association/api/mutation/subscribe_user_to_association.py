from __future__ import annotations

import strawberry

from association.api.context import Info
from association.api.types import SubscriptionResponse
from association.domain import services
from association.domain.entities.subscriptions import UserData
from association.domain.exceptions import AlreadySubscribed
from association.settings import TEST_USER_EMAIL, TEST_USER_ID


@strawberry.type
class AlreadySubscribedError:
    message: str = "You are already subscribed"


SubscribeUserResult = strawberry.union(
    "SubscribeUserResult", (SubscriptionResponse, AlreadySubscribedError)
)


@strawberry.mutation
async def subscribe_user_to_association(info: Info) -> SubscribeUserResult:
    user_data = UserData(email=TEST_USER_EMAIL, user_id=TEST_USER_ID)
    try:
        subscription = await services.subscribe_user_to_association(
            user_data, association_repository=info.context.association_repository
        )
        return SubscriptionResponse.from_domain(subscription)
    except AlreadySubscribed:
        return AlreadySubscribedError()
