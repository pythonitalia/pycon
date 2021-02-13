from typing import Optional

import strawberry
from strawberry import ID

from users.admin_api.context import Info
from users.admin_api.permissions import IsStaff
from users.admin_api.types import SearchResults, User


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsStaff])
    async def me(self, info: Info) -> Optional[User]:
        me = await info.context.users_repository.get_by_id(info.context.request.user.id)
        return User.from_domain(me) if me else None

    @strawberry.field(permission_classes=[IsStaff])
    async def users(self, info: Info) -> list[User]:
        all_users = await info.context.users_repository.get_users()
        return [User.from_domain(user) for user in all_users]

    @strawberry.field(permission_classes=[IsStaff])
    async def user(self, info: Info, id: ID) -> Optional[User]:
        user = await info.context.users_repository.get_by_id(int(id))
        return User.from_domain(user) if user else None

    @strawberry.field(permission_classes=[IsStaff])
    async def search(self, info: Info, query: str) -> SearchResults:
        users = await info.context.users_repository.search(query)
        return SearchResults.from_domain(users)
