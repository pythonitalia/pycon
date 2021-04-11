from typing import Any

import strawberry
from strawberry.types import Info

from api.context import Context
from association.domain import services
from association.domain.exceptions import CustomerNotAvailable
from association.settings import TEST_USER_EMAIL, TEST_USER_ID
from association_membership.domain.entities import UserData


@strawberry.type
class CustomerNotAvailableError:
    message: str = "Customer not available"


@strawberry.type
class CustomerPortalResponse:
    billing_portal_url: str


CustomerPortalResult = strawberry.union(
    "CustomerPortalResult", (CustomerPortalResponse, CustomerNotAvailableError)
)


@strawberry.mutation
async def manage_user_association_subscription(
    info: Info[Context, Any]
) -> CustomerPortalResult:
    # TODO ger UserData from authenticated User
    user_data = UserData(email=TEST_USER_EMAIL, user_id=TEST_USER_ID)

    try:
        billing_portal_url = await services.manage_user_association_subscription(
            user_data, association_repository=info.context.association_repository
        )
        return CustomerPortalResponse(billing_portal_url=billing_portal_url)
    except CustomerNotAvailable:
        return CustomerNotAvailableError()
