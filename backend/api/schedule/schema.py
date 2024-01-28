from typing import Optional
from api.context import Info

import strawberry
from strawberry import ID

from api.schedule.types import ScheduleInvitation
from api.submissions.permissions import IsSubmissionSpeakerOrStaff
from schedule.models import ScheduleItem as ScheduleItemModel
from submissions.models import Submission as SubmissionModel

from ..permissions import IsAuthenticated


@strawberry.type
class ScheduleQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def schedule_invitation(
        self, info: Info, submission_id: ID
    ) -> Optional[ScheduleInvitation]:
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
            .exclude(status=ScheduleItemModel.STATUS.cancelled)
            .first()
        )

        if not schedule_item:
            return None

        return ScheduleInvitation.from_django_model(schedule_item)
