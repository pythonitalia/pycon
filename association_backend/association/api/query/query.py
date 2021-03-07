from typing import Optional

import strawberry
from association.api.context import Info
from association.api.types import SubscriptionResponse


@strawberry.type
class Query:
    @strawberry.field()  # permission_classes=[IsJWTAvailable])
    async def my_subscription(self, info: Info) -> Optional[SubscriptionResponse]:
        # user_id = decode_token(info.context.request.cookies.get(
        #     JWT_USERS_COOKIE_NAME)
        # ).id
        user_id = 12345
        subscription = await info.context.association_repository.get_subscription_by_user_id(
            user_id
        )
        print(f"subscription : {subscription}")
        return SubscriptionResponse.from_domain(subscription)
