from __future__ import annotations

from typing import Optional

import strawberry

from association.api.context import Info
from association.domain import services
from association.domain.entities import stripe as stripe_entities
from association.domain.entities.subscriptions import UserData
from association.domain.exceptions import (
    AlreadySubscribed,
    MultipleCustomerReturned,
    MultipleCustomerSubscriptionsReturned,
)
from association.settings import TEST_USER_EMAIL, TEST_USER_ID


@strawberry.type
class AlreadySubscribedError:
    message: str = "You are already subscribed"


@strawberry.type
class MultipleCustomerReturnedError:
    message: str = "It seems you have multiple profiles registered on Stripe with the same email. You will be contacted by the association in the coming days"


@strawberry.type
class MultipleCustomerSubscriptionsReturnedError:
    message: str = "It seems you have multiple subscriptions registered on Stripe with the same customer. You will be contacted by the association in the coming days"


@strawberry.type
class CheckoutSession:
    stripe_session_id: str
    stripe_subscription_id: Optional[str]
    stripe_customer_id: Optional[str]

    @classmethod
    def from_domain(
        cls, entity: stripe_entities.StripeCheckoutSession
    ) -> CheckoutSession:
        return cls(
            stripe_session_id=entity.id,
            stripe_subscription_id=entity.subscription_id,
            stripe_customer_id=entity.customer_id,
        )


SubscribeUserResult = strawberry.union(
    "SubscribeUserResult",
    (
        CheckoutSession,
        AlreadySubscribedError,
        MultipleCustomerReturnedError,
        MultipleCustomerSubscriptionsReturnedError,
    ),
)


@strawberry.mutation
async def subscribe_user_to_association(info: Info) -> SubscribeUserResult:
    user_data = UserData(email=TEST_USER_EMAIL, user_id=TEST_USER_ID)
    try:
        checkout_session = await services.subscribe_user_to_association(
            user_data, association_repository=info.context.association_repository
        )
        return CheckoutSession.from_domain(checkout_session)
    except AlreadySubscribed:
        return AlreadySubscribedError()
    except MultipleCustomerReturned:
        return MultipleCustomerReturnedError()
    except MultipleCustomerSubscriptionsReturned:
        return MultipleCustomerSubscriptionsReturnedError()
