from strawberry.permission import BasePermission

from api.models import APIToken
from voting.helpers import pastaporto_user_info_can_vote


class IsAuthenticated(BasePermission):
    message = "User not logged in"

    def has_permission(self, source, info, **kwargs):
        return (
            info.context.request.user.is_authenticated
            or info.context.request.pastaporto.is_authenticated
        )


class HasTokenPermission(BasePermission):
    message = "Invalid or no token provided"

    def has_permission(self, source, info, **kwargs):
        token = info.context.request.headers.get("X-Backend-Token")

        if token:
            return APIToken.objects.filter(token=token).exists()

        return False


class IsStaffPermission(BasePermission):
    message = "You need to be a staff user"

    def has_permission(self, source, info, **kwargs):
        pastaporto = info.context.request.pastaporto

        if not pastaporto.is_authenticated:
            return False

        return pastaporto.user_info.is_staff


class CanSeeSubmissions(BasePermission):
    message = "You need to have a ticket to see submissions"

    def has_permission(self, conference, info):
        pastaporto = info.context.request.pastaporto

        if not pastaporto.is_authenticated:
            return False

        return pastaporto_user_info_can_vote(pastaporto, conference)
