from strawberry.permission import BasePermission

from api.models import APIToken
from voting.helpers import check_if_user_can_vote


class IsAuthenticated(BasePermission):
    message = "User not logged in"

    def has_permission(self, source, info, **kwargs):
        return info.context.request.user.is_authenticated


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
        user = info.context.request.user

        if not user.is_authenticated:
            return False

        return user.is_staff


class CanSeeSubmissions(BasePermission):
    message = "You need to have a ticket to see submissions"

    def has_permission(self, conference, info):
        user = info.context.request.user

        if not user.is_authenticated:
            return False

        return check_if_user_can_vote(user, conference)


class CanEditSchedule(IsStaffPermission):
    message = "Cannot edit schedule"

    def has_permission(self, source, info, **kwargs):
        if not super().has_permission(source, info, **kwargs):
            return False

        from conferences.models import Conference

        conference_id = kwargs.get(
            "conferenceId", kwargs.get("input", {}).get("conferenceId")
        )
        assert conference_id

        conference = Conference.objects.filter(id=conference_id).first()
        assert conference

        user = info.context.request.user
        return user.has_perm("schedule.change_scheduleitem", conference)
