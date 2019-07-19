from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "User not logged in"

    def has_permission(self, info):
        return info.context.user.is_authenticated
