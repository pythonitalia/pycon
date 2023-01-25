from strawberry.permission import BasePermission

from api.permissions import HasTokenPermission
from submissions.models import Submission
from voting.helpers import pastaporto_user_info_can_vote
from voting.models.ranking import RankRequest


class CanSeeSubmissionRestrictedFields(BasePermission):
    message = "You can't see details for this submission"

    def has_permission(self, source, info, **kwargs):
        is_speaker_data = kwargs.pop("is_speaker_data", False)
        if HasTokenPermission().has_permission(source, info):
            return True

        conference = source.conference

        try:
            if conference.rankrequest and conference.rankrequest.is_public:
                return True
        except RankRequest.DoesNotExist:
            pass

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

        if is_speaker_data:
            return False

        if info.context._user_can_vote is not None:
            return info.context._user_can_vote

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

        return pastaporto_user_info_can_vote(
            pastaporto,
            submission.conference,
        )


class IsSubmissionSpeakerOrStaff(BasePermission):
    message = "Not authorized"

    def has_object_permission(self, info, submission):
        pastaporto = info.context.request.pastaporto
        user_info = pastaporto.user_info
        if user_info.is_staff:
            return True

        return submission.speaker_id == user_info.id
