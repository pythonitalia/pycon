import logging
from typing import Optional

import strawberry
from strawberry import ID

from users.internal_api.context import Info
from users.internal_api.types import User

logger = logging.getLogger(__name__)


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info: Info, id: ID) -> Optional[User]:
        logger.info(f"Internal api request to get user id {id} information")
        user = await info.context.users_repository.get_by_id(int(id))
        return User.from_domain(user) if user else None
