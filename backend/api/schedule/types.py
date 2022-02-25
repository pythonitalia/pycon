from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

import strawberry
from strawberry import LazyType

from api.languages.types import Language
from api.submissions.types import Submission
from schedule.models import ScheduleItem as ScheduleItemModel

if TYPE_CHECKING:  # pragma: no cover
    import api  # noqa
    from api.conferences.types import AudienceLevel, Conference  # noqa


@strawberry.type
class Room:
    id: strawberry.ID
    name: str
    conference: LazyType["Conference", "api.conferences.types"]
    type: str


@strawberry.federation.type(keys=["id"])
class ScheduleItemUser:
    id: strawberry.ID


@strawberry.type
class ScheduleItem:
    id: strawberry.ID
    conference: LazyType["Conference", "api.conferences.types"]
    title: str
    start: datetime
    end: datetime
    submission: Optional[Submission]
    slug: str
    description: str
    type: str
    duration: Optional[int]
    highlight_color: Optional[str]
    speakers: List[ScheduleItemUser]
    language: Language
    audience_level: Optional[LazyType["AudienceLevel", "api.conferences.types"]]

    @strawberry.field
    def rooms(self, info) -> List[Room]:
        return self.rooms.all()

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context.request.build_absolute_uri(self.image.url)


@strawberry.type
class ScheduleInvitationDate:
    id: strawberry.ID
    start: datetime
    end: datetime

    @classmethod
    def from_django(cls, schedule_item):
        hour_slot = schedule_item.slot.hour
        day = schedule_item.slot.day.day
        start = datetime.combine(day, hour_slot)
        duration = schedule_item.duration or schedule_item.slot.duration
        return cls(
            id=schedule_item.id, start=start, end=start + timedelta(minutes=duration)
        )


@strawberry.enum
class ScheduleInvitationOption(Enum):
    NO_ANSWER = "no_answer"
    CONFIRM = "confirm"
    MAYBE = "maybe"
    REJECT = "reject"
    CANT_ATTEND = "cant_attend"

    def to_schedule_item_status(self):
        if self == ScheduleInvitationOption.CONFIRM:
            return ScheduleItemModel.STATUS.confirmed

        if self == ScheduleInvitationOption.MAYBE:
            return ScheduleItemModel.STATUS.maybe

        if self == ScheduleInvitationOption.REJECT:
            return ScheduleItemModel.STATUS.rejected

        if self == ScheduleInvitationOption.CANT_ATTEND:
            return ScheduleItemModel.STATUS.cant_attend

    @staticmethod
    def from_schedule_item_status(schedule_item_status: str):
        if schedule_item_status == ScheduleItemModel.STATUS.waiting_confirmation:
            return ScheduleInvitationOption.NO_ANSWER

        if schedule_item_status == ScheduleItemModel.STATUS.confirmed:
            return ScheduleInvitationOption.CONFIRM

        if schedule_item_status == ScheduleItemModel.STATUS.maybe:
            return ScheduleInvitationOption.MAYBE

        if schedule_item_status == ScheduleItemModel.STATUS.rejected:
            return ScheduleInvitationOption.REJECT

        if schedule_item_status == ScheduleItemModel.STATUS.cant_attend:
            return ScheduleInvitationOption.CANT_ATTEND


@strawberry.type
class ScheduleInvitation:
    id: strawberry.ID
    option: ScheduleInvitationOption
    notes: str
    submission: Submission
    dates: List[ScheduleInvitationDate]

    @classmethod
    def from_django_model(cls, instance):
        return cls(
            id=instance.submission.hashid,
            option=ScheduleInvitationOption.from_schedule_item_status(instance.status),
            notes=instance.speaker_invitation_notes,
            submission=instance.submission,
            dates=[ScheduleInvitationDate.from_django(instance)],
        )
