from __future__ import annotations

import datetime

import strawberry
from association.api.context import Info
from association.api.types import SubscriptionResponse
from association.domain import services
from association.domain.entities.subscription_entities import UserData
from association.domain.exceptions import AlreadySubscribed


# ===========
# Validation Errors
# ==========
@strawberry.type
class AlreadySubscribedError:
    expiration_date: datetime.datetime
    message: str = "You are already subscribed"


# ===========
# Output
# ==========
CheckoutSessionResult = strawberry.union(
    "CheckoutSessionResult", (SubscriptionResponse, AlreadySubscribedError)
)


# ===========
# Mutation
# ==========
@strawberry.mutation
async def subscribe_user_to_association(info: Info) -> CheckoutSessionResult:
    # TODO We have to define the name of the JWT TOKEN KEY
    # try:
    #     user_data = await decode_token(info.context.request.cookies.get(JWT_USERS_COOKIE_NAME))
    # except PyJWTError as exc:
    #     # TODO Maybe it is better to have a less declarative output to avoid risks
    #     return JWTValidationError(msg=str(exc))

    user_data = UserData(email="fake.user@pycon.it", user_id=12345)

    try:
        subscription = await services.subscribe_user_to_association(
            user_data, association_repository=info.context.association_repository
        )
        return SubscriptionResponse.from_domain(subscription)
    except AlreadySubscribed as exc:
        return AlreadySubscribedError(expiration_date=exc.expiration_date)
