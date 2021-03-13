from pythonit_toolkit.pastaporto.entities import Credential
from strawberry import BasePermission


class IsStaff(BasePermission):
    message = "Unauthorized"

    def has_permission(self, source, info, **kwargs):
        return (
            Credential.AUTHENTICATED in info.context.request.auth.scopes
            and Credential.STAFF in info.context.request.auth.scopes
        )
