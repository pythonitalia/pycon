from typing import Any

import strawberry
from pythonit_toolkit.api.permissions import IsAuthenticated
from strawberry.types import Info

from api.context import Context
from association_membership.domain import exceptions
from association_membership.domain.services.manage_user_association_subscription import (
    manage_user_association_subscription as service_manage_user_association_subscription,
)


@strawberry.type
class CustomerNotAvailable:
    message: str = "Customer not available"


@strawberry.type
class CustomerPortalResponse:
    billing_portal_url: str


CustomerPortalResult = strawberry.union(
    "CustomerPortalResult", (CustomerPortalResponse, CustomerNotAvailable)
)


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def manage_user_subscription(info: Info[Context, Any]) -> CustomerPortalResult:
    try:
        billing_portal_url = await service_manage_user_association_subscription(
            info.context.request.user,
            customers_repository=info.context.customers_repository,
        )
        return CustomerPortalResponse(billing_portal_url=billing_portal_url)
    except (exceptions.CustomerNotAvailable, exceptions.NoSubscriptionAvailable):
        return CustomerNotAvailable()
