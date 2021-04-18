from __future__ import annotations

from typing import Any

import strawberry
from pythonit_toolkit.api.permissions import IsAuthenticated
from strawberry.types import Info

from api.context import Context
from association_membership.domain import exceptions
from association_membership.domain.services.subscribe_user_to_association import (
    subscribe_user_to_association as service_subscribe_user_to_association,
)


@strawberry.type
class AlreadySubscribed:
    message: str = "You are already subscribed"


@strawberry.type
class CheckoutSession:
    stripe_session_id: str

    @classmethod
    def from_domain(cls, stripe_session_id: str) -> CheckoutSession:
        return cls(
            stripe_session_id=stripe_session_id,
        )


SubscribeUserResult = strawberry.union(
    "SubscribeUserResult",
    (
        CheckoutSession,
        AlreadySubscribed,
    ),
)


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def subscribe_user_to_association(
    info: Info[Context, Any]
) -> SubscribeUserResult:
    try:
        checkout_session_id = await service_subscribe_user_to_association(
            info.context.request.user,
            customers_repository=info.context.customers_repository,
            association_repository=info.context.association_repository,
        )
        return CheckoutSession.from_domain(checkout_session_id)
    except exceptions.AlreadySubscribed:
        return AlreadySubscribed()
