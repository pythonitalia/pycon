from datetime import datetime
from enum import Enum

import strawberry
import strawberry_django

from submissions.api.types import Submission
from schedule import models


@strawberry_django.type(models.ScheduleItem)
class ScheduleInvitationDate:
    id: strawberry.auto
    start: datetime
    end: datetime

    @strawberry_django.field
    def duration(self) -> int:
        return self.duration or self.slot.duration


@strawberry.enum
class ScheduleInvitationOption(Enum):
    NO_ANSWER = "no_answer"
    CONFIRM = "confirm"
    MAYBE = "maybe"
    REJECT = "reject"
    CANT_ATTEND = "cant_attend"

    def to_schedule_item_status(self) -> str:
        return MAP_OPTION_TO_ITEM_STATUS[self]


MAP_OPTION_TO_ITEM_STATUS = {
    ScheduleInvitationOption.CONFIRM: models.ScheduleItem.STATUS.confirmed,
    ScheduleInvitationOption.MAYBE: models.ScheduleItem.STATUS.maybe,
    ScheduleInvitationOption.REJECT: models.ScheduleItem.STATUS.rejected,
    ScheduleInvitationOption.CANT_ATTEND: models.ScheduleItem.STATUS.cant_attend,
    ScheduleInvitationOption.NO_ANSWER: models.ScheduleItem.STATUS.waiting_confirmation,
}

MAP_ITEM_STATUS_TO_OPTION = {
    item: option for option, item in MAP_OPTION_TO_ITEM_STATUS.items()
}


@strawberry_django.type(models.ScheduleItem)
class ScheduleInvitation:
    id: strawberry.ID = strawberry_django.field(
        resolver=lambda self: self.submission.hashid,
        select_related=["submission"],
    )
    option: ScheduleInvitationOption = strawberry_django.field(
        resolver=lambda self: MAP_ITEM_STATUS_TO_OPTION[self.status],
        only=["status"],
    )
    notes: str = strawberry_django.field(field_name="speaker_invitation_notes")
    title: strawberry.auto
    submission: Submission

    @strawberry_django.field(
        only=["duration", "slot__duration", "slot__hour", "slot__day__day"],
        select_related=["slot__day"],
    )
    def dates(self) -> list[ScheduleInvitationDate]:
        return [self]
