from typing import List

import strawberry
from association.api.context import Info
from association.api.types import Subscription


@strawberry.type
class Query:
    @strawberry.field()  # permission_classes=[IsJWTAvailable])
    async def my_subscriptions(self, info: Info) -> List[Subscription]:
        # user_id = decode_token(info.context.request.cookies.get(
        #     JWT_USERS_COOKIE_NAME)
        # ).id
        user_id = "12345"
        subscriptions = await info.context.association_repository.list_subscriptions_by_user_id(
            user_id
        )
        print(f"subscriptions : {subscriptions}")
        return [Subscription.from_domain(obj) for obj in subscriptions]
