from conferences.models.conference import Conference
from strawberry.permission import BasePermission


class IsStaff(BasePermission):
    message = "Forbidden"

    def has_permission(self, source, info, **kwargs):
        user = info.context.request.user
        return user.is_authenticated and user.is_staff


class CanEditSchedule(IsStaff):
    message = "Cannot edit schedule"

    def has_permission(self, source, info, **kwargs):
        if not super().has_permission(source, info, **kwargs):
            return False

        conference_id = kwargs.get("conferenceId")
        conference = Conference.objects.filter(id=conference_id).first()
        user = info.context.request.user
        return user.has_perm("schedule.change_scheduleitem", conference)
