from django.db import transaction
from api.schedule.types import (
    ScheduleInvitationOption,
)
from submissions.models import Submission
from schedule.models import (
    ScheduleItem,
)
from typing import Union
from api.permissions import IsAuthenticated
from api.schedule.types import (
    ScheduleInvitation,
)
from api.submissions.permissions import IsSubmissionSpeakerOrStaff

from schedule.tasks import notify_new_schedule_invitation_answer_slack
import strawberry


@strawberry.input
class UpdateScheduleInvitationInput:
    submission_id: strawberry.ID
    option: ScheduleInvitationOption
    notes: str


@strawberry.type
class ScheduleInvitationNotFound:
    message: str = "Invitation not found"


@strawberry.mutation(permission_classes=[IsAuthenticated])
def update_schedule_invitation(
    self, info, input: UpdateScheduleInvitationInput
) -> Union[ScheduleInvitationNotFound, ScheduleInvitation]:
    submission = Submission.objects.get_by_hashid(input.submission_id)

    if not IsSubmissionSpeakerOrStaff().has_object_permission(info, submission):
        return ScheduleInvitationNotFound()

    # TODO We assume here that a submission can only be in one schedule item
    # since currently we do not schedule the same talk to appear multiple times
    # in the future this needs to be fixed :)
    schedule_item = (
        ScheduleItem.objects.filter(
            submission_id=submission.id,
            conference_id=submission.conference_id,
        )
        .exclude(status=ScheduleItem.STATUS.cancelled)
        .first()
    )

    if not schedule_item:
        return ScheduleInvitationNotFound()

    new_status = input.option.to_schedule_item_status()
    new_notes = input.notes

    if (
        schedule_item.status == new_status
        and schedule_item.speaker_invitation_notes == new_notes
    ):
        # If nothing changed, do nothing
        return ScheduleInvitation.from_django_model(schedule_item)

    with transaction.atomic():
        schedule_item.status = new_status
        schedule_item.speaker_invitation_notes = new_notes
        schedule_item.save()

    request = info.context.request
    invitation_admin_url = request.build_absolute_uri(
        schedule_item.get_invitation_admin_url()
    )

    schedule_item_admin_url = request.build_absolute_uri(schedule_item.get_admin_url())
    notify_new_schedule_invitation_answer_slack.delay(
        schedule_item_id=schedule_item.id,
        invitation_admin_url=invitation_admin_url,
        schedule_item_admin_url=schedule_item_admin_url,
    )
    return ScheduleInvitation.from_django_model(schedule_item)
