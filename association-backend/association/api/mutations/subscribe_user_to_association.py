from __future__ import annotations

from typing import Any, Optional

import strawberry
from strawberry.types import Info

from association.api.context import Context
from association.domain.entities import stripe as stripe_entities
from association.domain.exceptions import (
    AlreadySubscribed,
    MultipleCustomerReturned,
    MultipleCustomerSubscriptionsReturned,
)
from association.domain.services.subscribe_user_to_association import (
    subscribe_user_to_association as service_subscribe_user_to_association,
)
from association.settings import TEST_USER_EMAIL, TEST_USER_ID
from association_membership.domain.entities import UserData


@strawberry.type
class AlreadySubscribedError:
    message: str = "You are already subscribed"


@strawberry.type
class CheckoutSession:
    stripe_session_id: str
    # stripe_subscription_id: Optional[str]
    # stripe_customer_id: Optional[str]

    @classmethod
    def from_domain(
        cls, entity: stripe_entities.StripeCheckoutSession
    ) -> CheckoutSession:
        return cls(
            stripe_session_id=entity.id,
            # stripe_subscription_id=entity.subscription_id,
            # stripe_customer_id=entity.customer_id,
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
    user_data = UserData(email=TEST_USER_EMAIL, user_id=TEST_USER_ID)
    try:
        checkout_session = await service_subscribe_user_to_association(
            user_data,
            customers_repository=info.context.customers_repository,
            association_repository=info.context.association_repository,
        )
        return CheckoutSession.from_domain(checkout_session)
    except AlreadySubscribed:
        return AlreadySubscribedError()
