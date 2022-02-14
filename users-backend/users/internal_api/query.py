import logging
from typing import Optional

import strawberry
from strawberry import ID

from users.internal_api.context import Info
from users.internal_api.permissions import IsService
from users.internal_api.types import User

logger = logging.getLogger(__name__)


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsService(["gateway", "pycon-backend"])])
    async def user(self, info: Info, id: ID) -> Optional[User]:
        logger.info("Internal api request to get user_id=%s information", id)
        user = await info.context.users_repository.get_by_id(int(id))
        return User.from_domain(user) if user else None

    @strawberry.field(permission_classes=[IsService(["pycon-backend"])])
    async def users_by_ids(self, info: Info, ids: list[ID]) -> list[User]:
        logger.info("Internal api request to get users=%s information", ids)
        users = await info.context.users_repository.get_batch_by_ids(
            [int(id) for id in ids]
        )
        return [User.from_domain(user) for user in users]

    @strawberry.field(permission_classes=[IsService(["pycon-backend"])])
    async def search_users(self, info: Info, query: str) -> list[User]:
        users = await info.context.users_repository.search(query)
        return [User.from_domain(user) for user in users]

    @strawberry.field(permission_classes=[IsService(["association-backend"])])
    async def user_by_email(self, info: Info, email: str) -> Optional[User]:
        user = await info.context.users_repository.get_by_email(email)
        return User.from_domain(user) if user else None

    @strawberry.field(permission_classes=[IsService(["pycon-backend"])])
    async def users_by_emails(self, info: Info, emails: list[str]) -> list[User]:
        users = await info.context.users_repository.get_batch_by_emails(emails)
        return [User.from_domain(user) for user in users]
