import strawberry
from api.context import Info
from api.permissions import IsAuthenticated
from api.types import User


@strawberry.field(permission_classes=[IsAuthenticated])
def me(info: Info) -> User:
    return User.from_domain(info.context.request.user)
