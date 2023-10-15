from strawberry.tools import create_type
import strawberry

from api.context import Info
from api.permissions import IsAuthenticated
from api.users.types import User


@strawberry.field(permission_classes=[IsAuthenticated])
def me(info: Info) -> User:
    return User.from_django_model(info.context.request.user)


UserQuery = create_type(
    "UserQuery",
    [
        me,
    ],
)
