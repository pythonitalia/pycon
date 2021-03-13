import strawberry

from users.api.context import Info
from users.api.permissions import IsAuthenticated
from users.api.types import User


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me(self, info: Info) -> User:
        me = await info.context.users_repository.get_by_id(info.context.request.user.id)
        return User.from_domain(me)
