from strawberry import BasePermission

from users.domain.entities import Credential


class IsStaff(BasePermission):
    message = "No"

    def has_permission(self, source, info, **kwargs):
        return (
            Credential.AUTHENTICATED in info.context.request.auth.scopes
            and Credential.STAFF in info.context.request.auth.scopes
        )
