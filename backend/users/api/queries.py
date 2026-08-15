import strawberry_django
from strawberry.tools import create_type

from api.context import Info
from api.permissions import IsAuthenticated
from users.api.types import User


@strawberry_django.field(permission_classes=[IsAuthenticated])
def me(info: Info) -> User:
    return info.context.request.user


UserQuery = create_type(
    "UserQuery",
    [
        me,
    ],
)
