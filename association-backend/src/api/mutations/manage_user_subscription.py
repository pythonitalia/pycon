from typing import Any

import strawberry
from pythonit_toolkit.api.permissions import IsAuthenticated
from strawberry.types import Info

from src.api.context import Context
from src.association_membership.domain import exceptions
from src.association_membership.domain.services.manage_user_association_subscription import (
    manage_user_association_subscription as service_manage_user_association_subscription,
)


@strawberry.type
class NoSubscription:
    message: str = "No subscription to manage"


@strawberry.type
class CustomerPortalResponse:
    billing_portal_url: str


CustomerPortalResult = strawberry.union(
    "CustomerPortalResult", (CustomerPortalResponse, NoSubscription)
)


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def manage_user_subscription(info: Info[Context, Any]) -> CustomerPortalResult:
    try:
        billing_portal_url = await service_manage_user_association_subscription(
            info.context.request.user,
        )
        return CustomerPortalResponse(billing_portal_url=billing_portal_url)
    except (exceptions.CustomerNotAvailable, exceptions.NoSubscriptionAvailable):
        return NoSubscription()
