from strawberry.permission import BasePermission

from users.api.context import Info
from users.domain.entities import Credential


class IsAuthenticated(BasePermission):
    message = "Not authenticated"

    def has_permission(self, source, info: Info, **kwargs):
        return Credential.AUTHENTICATED in info.context.request.auth.scopes
