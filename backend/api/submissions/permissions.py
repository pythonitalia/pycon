from strawberry.permission import BasePermission

from api.permissions import HasTokenPermission
from voting.helpers import check_if_user_can_vote
from voting.models.ranking import RankRequest


class CanSeeSubmissionRestrictedFields(BasePermission):
    message = "You can't see details for this submission"

    def has_permission(self, source, info, **kwargs):
        is_speaker_data = kwargs.pop("is_speaker_data", False)
        if HasTokenPermission().has_permission(source, info):
            return True

        if source.schedule_items.exists():  # pragma: no cover
            return True

        conference = source.conference

        try:
            if conference.rankrequest and conference.rankrequest.is_public:
                return True
        except RankRequest.DoesNotExist:
            pass

        user = info.context.request.user

        if not user.is_authenticated:
            return False

        if user.is_staff or source.speaker_id == user.id:
            return True

        if conference.is_voting_closed:
            return False

        if is_speaker_data:
            return False

        if info.context._user_can_vote is not None:
            return info.context._user_can_vote

        return check_if_user_can_vote(user, conference)


class CanSeeSubmissionPrivateFields(BasePermission):
    message = "You can't see the private fields for this submission"

    def has_permission(self, source, info):
        user = info.context.request.user

        if not user.is_authenticated:
            return False

        return user.is_staff or source.speaker_id == user.id


class IsSubmissionSpeakerOrStaff(BasePermission):
    message = "Not authorized"

    def has_object_permission(self, info, submission):
        user = info.context.request.user

        if user.is_staff:
            return True

        return submission.speaker_id == user.id
