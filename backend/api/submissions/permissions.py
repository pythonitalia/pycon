from strawberry.permission import BasePermission

from api.permissions import HasTokenPermission
from pretix.db import user_has_admission_ticket
from submissions.models import Submission
from voting.helpers import pastaporto_user_info_can_vote


class CanSeeSubmissionRestrictedFields(BasePermission):
    message = "You can't see details for this submission"

    def has_permission(self, source, info):
        if HasTokenPermission().has_permission(source, info):
            return True

        conference = source.conference

        if source.schedule_items.exists():  # pragma: no cover
            return True

        pastaporto = info.context.request.pastaporto

        if not pastaporto.is_authenticated:
            return False

        user_info = info.context.request.user

        if user_info.is_staff or source.speaker_id == user_info.id:
            return True

        if conference.is_voting_closed:
            return False

        return pastaporto_user_info_can_vote(pastaporto, conference)


class CanSeeSubmissionPrivateFields(BasePermission):
    message = "You can't see the private fields for this submission"

    def has_permission(self, source, info):
        pastaporto = info.context.request.pastaporto

        if not pastaporto.is_authenticated:
            return False

        return (
            pastaporto.user_info.is_staff
            or source.speaker_id == pastaporto.user_info.id
        )


class CanSendComment(BasePermission):
    message = "You can't send a comment"

    def has_permission(self, source, info):
        pastaporto = info.context.request.pastaporto
        user_info = pastaporto.user_info

        if user_info.is_staff:
            return True

        input = info.context.input
        submission = Submission.objects.get_by_hashid(input.submission)

        if submission.speaker_id == user_info.id:
            return True

        if Submission.objects.filter(
            speaker_id=user_info.id, conference=submission.conference
        ).exists():
            return True

        return user_has_admission_ticket(
            user_info.email, submission.conference.pretix_event_id
        )
