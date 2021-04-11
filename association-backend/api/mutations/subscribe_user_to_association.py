from __future__ import annotations

from typing import Any

import strawberry
from strawberry.types import Info

from api.context import Context
from association.domain.entities import stripe as stripe_entities
from association.domain.exceptions import AlreadySubscribed
from association.domain.services.subscribe_user_to_association import (
    subscribe_user_to_association as service_subscribe_user_to_association,
)


@strawberry.type
class AlreadySubscribedError:
    message: str = "You are already subscribed"


@strawberry.type
class CheckoutSession:
    stripe_session_id: str

    @classmethod
    def from_domain(
        cls, entity: stripe_entities.StripeCheckoutSession
    ) -> CheckoutSession:
        return cls(
            stripe_session_id=entity.id,
        )


SubscribeUserResult = strawberry.union(
    "SubscribeUserResult",
    (
        CheckoutSession,
        AlreadySubscribedError,
    ),
)


@strawberry.mutation
async def subscribe_user_to_association(
    info: Info[Context, Any]
) -> SubscribeUserResult:
    try:
        checkout_session = await service_subscribe_user_to_association(
            info.context.request.user,
            customers_repository=info.context.customers_repository,
            association_repository=info.context.association_repository,
        )
        return CheckoutSession.from_domain(checkout_session)
    except AlreadySubscribed:
        return AlreadySubscribedError()
