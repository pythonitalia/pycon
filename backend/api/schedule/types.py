from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

import strawberry

from api.languages.types import Language
from api.participants.types import Participant
from api.submissions.types import Submission
from participants.models import Participant as ParticipantModel
from schedule.models import ScheduleItem as ScheduleItemModel
from conferences.models import Keynote as KeynoteModel
from typing import Annotated

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import AudienceLevel, Conference, Keynote


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
    streaming_url: str
    slido_url: str


@strawberry.federation.type(keys=["id"])
class ScheduleItemUser:
    id: strawberry.ID
    conference_code: strawberry.Private[str]

    @strawberry.field
    def participant(self) -> Optional[Participant]:
        participant = ParticipantModel.objects.filter(
            user_id=self.id,
            conference__code=self.conference_code,
        ).first()

        if not participant:
            return None

        return Participant.from_model(participant)


@strawberry.type
class ScheduleItem:
    id: strawberry.ID
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: str
    start: datetime
    end: datetime
    status: str
    submission: Optional[Submission]
    slug: str
    description: str
    type: str
    duration: Optional[int]
    highlight_color: Optional[str]
    language: Language
    audience_level: Optional[
        Annotated["AudienceLevel", strawberry.lazy("api.conferences.types")]
    ]

    @strawberry.field
    async def has_limited_capacity(self) -> bool:
        return self.attendees_total_capacity is not None

    @strawberry.field
    async def has_spaces_left(self) -> bool:
        if self.attendees_total_capacity is None:
            return True

        return self.attendees_total_capacity - await self.attendees.acount() > 0

    @strawberry.field
    async def spaces_left(self) -> int:
        if self.attendees_total_capacity is None:
            return 0

        return self.attendees_total_capacity - await self.attendees.acount()

    @strawberry.field
    async def user_has_spot(self, info) -> bool:
        user_id = info.context.request.user.id
        return await self.attendees.filter(user_id=user_id).aexists()

    @strawberry.field
    async def speakers(self) -> List[ScheduleItemUser]:
        speakers = []

        all_speakers = await self.speakers

        for speaker in all_speakers:
            speakers.append(
                ScheduleItemUser(id=speaker, conference_code=self.conference.code)
            )

        return speakers

    @strawberry.field
    async def keynote(
        self,
    ) -> Optional[Annotated["Keynote", strawberry.lazy("api.conferences.types")]]:
        from api.conferences.types import Keynote

        if not self.keynote_id:
            return None

        keynote = await KeynoteModel.objects.prefetch_related(
            "speakers", "conference"
        ).aget(id=self.keynote_id)
        schedule_item = await ScheduleItemModel.objects.select_related(
            "slot", "slot__day"
        ).aget(keynote_id=self.keynote_id)
        return Keynote.from_django_model(keynote, schedule_item)

    @strawberry.field
    async def rooms(self, info) -> List[Room]:
        return [room async for room in self.rooms.all()]

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context.request.build_absolute_uri(self.image.url)

    @strawberry.field
    async def slido_url(self, info) -> str:
        if self.slido_url:
            return self.slido_url

        # For multi-room items we use the first room slido url
        room = await self.rooms.afirst()
        first_room = await self.slot.day.added_rooms.aget(room_id=room)
        return first_room.slido_url


@strawberry.type
class ScheduleInvitationDate:
    id: strawberry.ID
    start: datetime
    end: datetime

    @classmethod
    def from_django(cls, schedule_item):
        return cls(
            id=schedule_item.id, start=schedule_item.start, end=schedule_item.end
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
    dates: List[ScheduleInvitationDate]

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
