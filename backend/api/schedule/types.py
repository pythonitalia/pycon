from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Union

import strawberry
from strawberry import LazyType

from api.languages.types import Language
from api.submissions.types import Submission
from schedule.models import ScheduleItem as ScheduleItemModel

if TYPE_CHECKING:  # pragma: no cover
    import api  # noqa
    from api.conferences.types import AudienceLevel, Conference, Keynote  # noqa


@strawberry.type
class Room:
    id: strawberry.ID
    name: str
    type: str


@strawberry.type
class DayRoom:
    id: strawberry.ID
    name: str
    type: str
    streaming_link: str


@strawberry.federation.type(keys=["id"])
class ScheduleItemUser:
    id: strawberry.ID


@strawberry.type
class ScheduleItemNamedUser:
    full_name: str


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
    language: Language
    audience_level: Optional[LazyType["AudienceLevel", "api.conferences.types"]]

    @strawberry.field
    def has_limited_capacity(self) -> bool:
        return self.attendees_total_capacity is not None

    @strawberry.field
    def has_spaces_left(self) -> bool:
        if self.attendees_total_capacity is None:
            return True

        return self.attendees_total_capacity - self.attendees.count() > 0

    @strawberry.field
    def spaces_left(self) -> int:
        if self.attendees_total_capacity is None:
            return 0

        return self.attendees_total_capacity - self.attendees.count()

    @strawberry.field
    def user_has_spot(self, info) -> bool:
        user_id = info.context.request.user.id
        return self.attendees.filter(user_id=user_id).exists()

    @strawberry.field
    def speakers(self) -> List[Union[ScheduleItemUser, ScheduleItemNamedUser]]:
        speakers = []
        for speaker in self.speakers:
            if not speaker.id:
                speakers.append(ScheduleItemNamedUser(full_name=speaker.full_name))
            else:
                speakers.append(ScheduleItemUser(id=speaker.id))

        return speakers

    @strawberry.field
    def keynote(self) -> Optional[LazyType["Keynote", "api.conferences.types"]]:
        from api.conferences.types import Keynote

        if not self.keynote_id:
            return None

        return Keynote.from_django_model(self.keynote)

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
