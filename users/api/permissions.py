from api.context import Info
from auth.entities import Credential
from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "Not authenticated"

    def has_permission(self, source, info: Info, **kwargs):
        return Credential.AUTHENTICATED in info.context.request.auth.scopes
