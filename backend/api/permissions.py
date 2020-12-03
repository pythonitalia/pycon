from api.models import APIToken
from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "User not logged in"

    def has_permission(self, source, info, **kwargs):
        return info.context.request.user.is_authenticated


class HasTokenPermission(BasePermission):
    message = "Invalid or no token provided"

    def has_permission(self, source, info, **kwargs):
        token = info.context.request.headers.get("Authorization")

        if token:
            token = token.split(" ")[1]

            return APIToken.objects.filter(token=token).exists()

        return False


class IsStaffPermission(BasePermission):
    message = "You need to be a staff user"

    def has_permission(self, source, info, **kwargs):
        user = info.context.request.user

        if not user.is_authenticated:
            return False

        return user.is_staff or user.is_superuser


class CanSeeSubmissions(BasePermission):
    message = "You need to have a ticket to see submissions"

    def has_permission(self, conference, info):
        user = info.context.request.user

        if not user.is_authenticated:
            return False

        return user.can_vote(conference)
