from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "User not logged in"

    def has_permission(self, source, info, **kwargs):
        return info.context["request"].user.is_authenticated
