import datetime

import pydantic
import strawberry
from association.api.context import Info
from association.api.types import Subscription
from association.domain import entities, services
from association.domain.exceptions import AlreadySubscribed

# ===========
# Input
# ==========


class UserData(pydantic.BaseModel):
    email: str
    user_id: str


# ===========
# Validation Errors
# ==========
@strawberry.type
class AlreadySubscribedError:
    expiration_date: datetime.datetime
    message: str = "You are already subscribed"


@strawberry.type
class SubscriptionResponse:
    # TODO return subscription
    subscription: Subscription

    @classmethod
    def from_domain(
        cls, subscription_entity: entities.Subscription
    ) -> "SubscriptionResponse":
        return cls(subscription=Subscription.from_domain(subscription_entity))


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
async def do_checkout(info: Info) -> CheckoutSessionResult:
    # TODO We have to define the name of the JWT TOKEN KEY
    # try:
    #     user_data = await decode_token(info.context.request.cookies.get(JWT_USERS_COOKIE_NAME))
    # except PyJWTError as exc:
    #     # TODO Maybe it is better to have a less declarative output to avoid risks
    #     return JWTValidationError(msg=str(exc))

    user_data = UserData(email="fake.user@pycon.it", user_id=12345)

    try:
        subscription = await services.do_checkout(
            user_data, association_repository=info.context.association_repository
        )
        return SubscriptionResponse.from_domain(subscription)
    except AlreadySubscribed as exc:
        return AlreadySubscribedError(expiration_date=exc.expiration_date)
