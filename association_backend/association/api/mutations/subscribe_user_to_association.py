from __future__ import annotations

from datetime import datetime
from typing import Optional

import strawberry

from association.api.context import Info
from association.domain import entities, services
from association.domain.entities.subscriptions import UserData
from association.domain.exceptions import AlreadySubscribed, MultipleCustomerReturned
from association.settings import TEST_USER_EMAIL, TEST_USER_ID


@strawberry.type
class AlreadySubscribedError:
    message: str = "You are already subscribed"


@strawberry.type
class MultipleCustomerReturnedError:
    message: str = "It seems you have multiple profiles registered on Stripe with the same email. You will be contacted by the association in the coming days"


@strawberry.type
class Subscription:
    user_id: int
    creation_date: datetime
    state: str
    stripe_session_id: str
    stripe_subscription_id: Optional[str]
    stripe_customer_id: Optional[str]

    @classmethod
    def from_domain(cls, entity: entities.Subscription) -> Subscription:
        return cls(
            user_id=entity.user_id,
            creation_date=entity.creation_date,
            stripe_subscription_id=entity.stripe_subscription_id,
            stripe_customer_id=entity.stripe_customer_id,
            state=entity.state,
            stripe_session_id=entity.stripe_session_id,
        )


SubscribeUserResult = strawberry.union(
    "SubscribeUserResult",
    (Subscription, AlreadySubscribedError, MultipleCustomerReturnedError),
)


@strawberry.mutation
async def subscribe_user_to_association(info: Info) -> SubscribeUserResult:
    user_data = UserData(email=TEST_USER_EMAIL, user_id=TEST_USER_ID)
    try:
        subscription = await services.subscribe_user_to_association(
            user_data, association_repository=info.context.association_repository
        )
        return Subscription.from_domain(subscription)
    except AlreadySubscribed:
        return AlreadySubscribedError()
    except MultipleCustomerReturned:
        return MultipleCustomerReturnedError()
