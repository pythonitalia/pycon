from strawberry.permission import BasePermission

import pretix
from conferences.models.conference import Conference


class IsTicketOwner(BasePermission):
    message = "You are not allowed to update this ticket."

    def has_permission(self, source, info, **kwargs):
        pastaporto = info.context.request.pastaporto

        if not pastaporto.is_authenticated:
            return False

        conference = Conference.objects.get(code=kwargs["conferenceCode"])
        if not conference:
            return False

        email = info.context.request.user.email
        if not pretix.is_ticket_owner(conference, email, kwargs["input"]["id"]):
            return False

        return True
