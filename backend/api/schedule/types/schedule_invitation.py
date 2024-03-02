from datetime import datetime
from enum import Enum

import strawberry

from api.submissions.types import Submission
from schedule.models import ScheduleItem as ScheduleItemModel


@strawberry.type
class ScheduleInvitationDate:
    id: strawberry.ID
    start: datetime
    end: datetime
    duration: int

    @classmethod
    def from_django(cls, schedule_item):
        duration = schedule_item.duration or schedule_item.slot.duration
        return cls(
            id=schedule_item.id,
            start=schedule_item.start,
            end=schedule_item.end,
            duration=duration,
        )


@strawberry.enum
class ScheduleInvitationOption(Enum):
    NO_ANSWER = "no_answer"
    CONFIRM = "confirm"
    MAYBE = "maybe"
    REJECT = "reject"
    CANT_ATTEND = "cant_attend"

    def to_schedule_item_status(self):
        return MAP_OPTION_TO_ITEM_STATUS.get(self)

    @staticmethod
    def from_schedule_item_status(schedule_item_status: str):
        return MAP_ITEM_STATUS_TO_OPTION.get(schedule_item_status)


MAP_OPTION_TO_ITEM_STATUS = {
    ScheduleInvitationOption.CONFIRM: ScheduleItemModel.STATUS.confirmed,
    ScheduleInvitationOption.MAYBE: ScheduleItemModel.STATUS.maybe,
    ScheduleInvitationOption.REJECT: ScheduleItemModel.STATUS.rejected,
    ScheduleInvitationOption.CANT_ATTEND: ScheduleItemModel.STATUS.cant_attend,
    ScheduleInvitationOption.NO_ANSWER: ScheduleItemModel.STATUS.waiting_confirmation,
}

MAP_ITEM_STATUS_TO_OPTION = {
    item: option for option, item in MAP_OPTION_TO_ITEM_STATUS.items()
}


@strawberry.type
class ScheduleInvitation:
    id: strawberry.ID
    option: ScheduleInvitationOption
    notes: str
    title: str
    submission: Submission
    dates: list[ScheduleInvitationDate]

    @classmethod
    def from_django_model(cls, instance):
        return cls(
            id=instance.submission.hashid,
            title=instance.title,
            option=ScheduleInvitationOption.from_schedule_item_status(instance.status),
            notes=instance.speaker_invitation_notes,
            submission=instance.submission,
            dates=[ScheduleInvitationDate.from_django(instance)],
        )
