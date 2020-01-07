from api.models import APIToken
from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "User not logged in"

    def has_permission(self, source, info, **kwargs):
        return info.context["request"].user.is_authenticated


class HasTokenPermission(BasePermission):
    message = "Invalid or no token provided"

    def has_permission(self, source, info, **kwargs):
        token = info.context["request"].headers.get("Authorization")

        if token:
            token = token.split(" ")[1]

            return APIToken.objects.filter(token=token).exists()

        return False
