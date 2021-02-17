from association.api.context import Info
from association.settings import JWT_USERS_COOKIE_NAME
from strawberry.permission import BasePermission


class IsJWTAvailable(BasePermission):
    message = "JWT Not Available"

    def has_permission(self, source, info: Info, **kwargs):
        return info.context.request.cookies.get(JWT_USERS_COOKIE_NAME, None) is not None
