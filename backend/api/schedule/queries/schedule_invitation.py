from api.context import Info
from schedule.models import ScheduleItem as ScheduleItemModel
from api.submissions.permissions import IsSubmissionSpeakerOrStaff
from submissions.models import Submission as SubmissionModel
import strawberry
from api.schedule.types.schedule_invitation import ScheduleInvitation
from api.permissions import IsAuthenticated


@strawberry.field(permission_classes=[IsAuthenticated])
def schedule_invitation(
    info: Info, submission_id: strawberry.ID
) -> ScheduleInvitation | None:
    submission = SubmissionModel.objects.get_by_hashid(submission_id)

    if not IsSubmissionSpeakerOrStaff().has_object_permission(info, submission):
        return None

    # TODO: A submission could be added to multiple schedule item
    # in the future we should support it
    schedule_item = (
        ScheduleItemModel.objects.filter(
            conference_id=submission.conference_id,
            submission_id=submission.id,
        )
        .prefetch_related(
            "submission",
            "submission__duration",
            "slot",
            "slot__day",
        )
        .exclude(status=ScheduleItemModel.STATUS.cancelled)
        .first()
    )

    if not schedule_item:
        return None

    return ScheduleInvitation.from_django_model(schedule_item)
