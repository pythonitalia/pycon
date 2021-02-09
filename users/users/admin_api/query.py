from typing import Optional

import strawberry
from strawberry import ID

from users.admin_api.context import Info
from users.admin_api.permissions import IsStaff
from users.admin_api.types import User


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsStaff])
    async def users(self, info: Info) -> list[User]:
        all_users = await info.context.users_repository.get_users()
        return [User.from_domain(user) for user in all_users]

    @strawberry.field(permission_classes=[IsStaff])
    async def user(self, info: Info, id: ID) -> Optional[User]:
        user = await info.context.users_repository.get_by_id(int(id))
        return User.from_domain(user) if user else None
