from __future__ import annotations

import pydantic
import strawberry
from association.api.builder import create_validation_error_type
from association.api.context import Info
from association.api.mutation.types import PydanticError
from association.api.types import SubscriptionRequest
from association.domain import entities, services
from association.domain.services import SubscriptionRequestInput
from association.domain.services.create_stripe_checkout_session import (
    StripeCreateCheckoutInput,
)
from association.domain.services.get_customer_from_stripe import StripeCustomerInput

# ===========
# Input
# ==========


# ===========
# Validation Errors
# ==========
@strawberry.type
class CreateStripeCheckoutErrors:
    user_email: PydanticError = None
    user_id: PydanticError = None
    price_id: PydanticError = None


CreateStripeCheckoutValidationError = create_validation_error_type(
    "CreateStripeCheckout", CreateStripeCheckoutErrors
)


@strawberry.type
class JWTErrors:
    msg: PydanticError = None


JWTValidationError = create_validation_error_type("JWT", JWTErrors)


@strawberry.type
class StripeCheckoutCreated:
    subscription_request: SubscriptionRequest

    @classmethod
    def from_domain(
        cls, subscription_request_entity: entities.SubscriptionRequest
    ) -> StripeCheckoutCreated:
        return cls(
            subscription_request=SubscriptionRequest.from_domain(
                subscription_request_entity
            )
        )


# ===========
# Output
# ==========
CreateStripeCheckoutResult = strawberry.union(
    "CreateStripeCheckoutResult",
    (StripeCheckoutCreated, CreateStripeCheckoutValidationError, JWTValidationError),
)


class UserData(pydantic.BaseModel):
    email: str
    user_id: str


# ===========
# Mutation
# ==========
@strawberry.mutation
async def setup_stripe_checkout(info: Info) -> CreateStripeCheckoutResult:
    # TODO We have to define the name of the JWT TOKEN KEY
    # try:
    #     user_data = await decode_token(info.context.request.cookies.get(JWT_USERS_COOKIE_NAME))
    # except PyJWTError as exc:
    #     # TODO Maybe it is better to have a less declarative output to avoid risks
    #     return JWTValidationError(msg=str(exc))

    user_data = UserData(email="gaetanodonghia@gmail.com", user_id="12345")

    try:
        customer = await services.get_customer_from_stripe(
            StripeCustomerInput(email=user_data.email)
        )
    except pydantic.ValidationError as exc:
        return CreateStripeCheckoutValidationError.from_validation_error(exc)

    try:
        checkout_session = await services.create_checkout_session(
            StripeCreateCheckoutInput(
                customer_email=user_data.email,
                customer_id=customer.id if customer else "",
                # price_id=request_data.price_id
            )
        )
    except pydantic.ValidationError as exc:
        return CreateStripeCheckoutValidationError.from_validation_error(exc)

    try:
        input_model = SubscriptionRequestInput(
            session_id=checkout_session.id,
            customer_id=checkout_session.customer_id,
            user_id=user_data.user_id,
        )
        subscription_request = await services.create_subscription_request(
            input_model, association_repository=info.context.association_repository
        )
    except pydantic.ValidationError as exc:
        return CreateStripeCheckoutValidationError.from_validation_error(exc)

    return StripeCheckoutCreated.from_domain(subscription_request)
