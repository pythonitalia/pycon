from pythonit_toolkit.pastaporto.entities import Credential
from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "Not authenticated"

    def has_permission(self, source, info, **kwargs):
        return Credential.AUTHENTICATED in info.context.request.auth.scopes
