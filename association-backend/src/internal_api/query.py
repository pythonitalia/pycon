import logging

import strawberry
from strawberry import ID

from src.internal_api.context import Info
from src.internal_api.permissions import IsService

logger = logging.getLogger(__name__)


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsService(["pycon-backend"])])
    async def user_id_is_member(self, info: Info, id: ID) -> bool:
        if not id:
            raise ValueError("Invalid ID")

        parsed_id = int(id)
        logger.info(
            "Internal api request to check if user_id=%s is a member", parsed_id
        )
        subscription = await info.context.association_repository.get_user_subscription(
            parsed_id
        )
        return subscription.is_active if subscription else False
