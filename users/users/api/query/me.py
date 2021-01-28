import strawberry
from users.api.context import Info
from users.api.permissions import IsAuthenticated
from users.api.types import User


@strawberry.field(permission_classes=[IsAuthenticated])
def me(info: Info) -> User:
    return User.from_domain(info.context.request.user)
