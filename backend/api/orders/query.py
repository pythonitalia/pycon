from typing import Optional

import strawberry
from api.permissions import IsAuthenticated
from api.pretix.query import get_order
from api.pretix.types import PretixOrder
from conferences.models import Conference


@strawberry.type
class OrdersQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def order(self, info, conference_code: str, code: str) -> Optional[PretixOrder]:
        conference = Conference.objects.get(code=conference_code)

        user = info.context.request.user
        order = get_order(conference, code)

        if not order:
            return None

        if user.email != order.email:
            return None

        return order
