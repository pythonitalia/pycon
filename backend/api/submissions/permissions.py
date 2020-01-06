from pretix.db import user_has_admission_ticket
from strawberry.permission import BasePermission


class CanSeeSubmissionTicketDetail(BasePermission):
    message = "You can't see details for this submission"

    def has_permission(self, source, info):
        user = info.context["request"].user

        if not user.is_authenticated:
            return False

        if user.is_staff or source.speaker == user:
            return True

        user_has_ticket = user_has_admission_ticket(
            user.email, source.conference.pretix_event_id
        )

        return user_has_ticket


class CanSeeSubmissionPrivateFields(BasePermission):
    message = "You can't see the private fields for this submission"

    def has_permission(self, source, info):
        user = info.context["request"].user

        if not user.is_authenticated:
            return False

        return user.is_staff or source.speaker == user
