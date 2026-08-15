import strawberry
import strawberry_django

from api.context import Info
from api.permissions import IsAuthenticated
from schedule.api.types.schedule_invitation import ScheduleInvitation
from submissions.api.permissions import IsSubmissionSpeakerOrStaff
from schedule import models as schedule_models
from submissions import models as submission_models


@strawberry_django.field(permission_classes=[IsAuthenticated])
def schedule_invitation(
    info: Info, submission_id: strawberry.ID
) -> ScheduleInvitation | None:
    submission = submission_models.Submission.objects.get_by_hashid(submission_id)

    if not IsSubmissionSpeakerOrStaff().has_object_permission(info, submission):
        return None

    # TODO: A submission could be added to multiple schedule item
    # in the future we should support it
    return schedule_models.ScheduleItem.objects.filter(
        conference_id=submission.conference_id,
        submission_id=submission.id,
    ).exclude(status=schedule_models.ScheduleItem.STATUS.cancelled)
