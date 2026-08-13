from api.context import Info
from api.schedule.optimization import (
    ATTENDEES_COUNT_ANNOTATION,
    CAPACITY_ANNOTATION,
    USER_HAS_SPOT_ANNOTATION,
    attendees_count_annotation,
    capacity_annotation,
    schedule_item_speakers,
    user_has_spot_annotation,
)
from api.participants.types import Participant
from participants.models import Participant as ParticipantModel
from typing import TYPE_CHECKING
from api.languages.types import Language
from api.permissions import IsStaffPermission
from datetime import datetime
from typing import Annotated
from api.schedule.types.schedule_item_user import ScheduleItemUser
from api.submissions.types import Submission
import strawberry
import strawberry_django
from schedule import models
from strawberry import auto
from api.schedule.types.room import Room

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import AudienceLevel, Conference, Keynote


def _capacity(schedule_item) -> int | None:
    if CAPACITY_ANNOTATION in schedule_item.__dict__:
        return getattr(schedule_item, CAPACITY_ANNOTATION)
    return schedule_item.actual_attendees_total_capacity


def _attendees_count(schedule_item) -> int:
    if ATTENDEES_COUNT_ANNOTATION in schedule_item.__dict__:
        return getattr(schedule_item, ATTENDEES_COUNT_ANNOTATION)
    return schedule_item.attendees.count()


@strawberry_django.type(models.ScheduleItem)
class ScheduleItem:
    id: auto
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: auto
    start: datetime
    end: datetime
    status: auto
    submission: Submission | None
    slug: str
    description: auto
    type: str
    duration: auto
    highlight_color: str | None
    language: Language
    audience_level: (
        Annotated["AudienceLevel", strawberry.lazy("api.conferences.types")] | None
    )
    youtube_video_id: str | None
    link_to: auto

    abstract: str
    elevator_pitch: str
    talk_manager: ScheduleItemUser | None = strawberry.field(
        permission_classes=[IsStaffPermission]
    )
    livestreaming_room: Room | None

    @strawberry_django.field(
        annotate={CAPACITY_ANNOTATION: capacity_annotation},
    )
    def has_limited_capacity(self) -> bool:
        return _capacity(self) is not None

    @strawberry_django.field(
        annotate={
            ATTENDEES_COUNT_ANNOTATION: attendees_count_annotation,
            CAPACITY_ANNOTATION: capacity_annotation,
        },
    )
    def has_spaces_left(self) -> bool:
        capacity = _capacity(self)
        if capacity is None:
            return True

        return capacity - _attendees_count(self) > 0

    @strawberry_django.field(
        annotate={
            ATTENDEES_COUNT_ANNOTATION: attendees_count_annotation,
            CAPACITY_ANNOTATION: capacity_annotation,
        },
    )
    def spaces_left(self) -> int:
        capacity = _capacity(self)
        if capacity is None:
            return 0

        return capacity - _attendees_count(self)

    @strawberry_django.field(
        annotate={USER_HAS_SPOT_ANNOTATION: user_has_spot_annotation},
    )
    def user_has_spot(self, info: Info) -> bool:
        if USER_HAS_SPOT_ANNOTATION in self.__dict__:
            return getattr(self, USER_HAS_SPOT_ANNOTATION)

        user_id = info.context.request.user.id
        return self.attendees.filter(user_id=user_id).exists()

    @strawberry.field
    def user_is_talk_manager(self, info: Info) -> bool:
        if not (user_id := info.context.request.user.id):
            return False

        return self.talk_manager_id == user_id

    @strawberry.field
    def speakers(self, info: Info) -> list[ScheduleItemUser]:
        speakers = []

        # TODO: Find a better solution
        participants_data = info.context._participants_data
        if not participants_data:
            participants_data = {
                participant.user_id: participant
                for participant in ParticipantModel.objects.filter(
                    user_id__in=[
                        speaker.id for speaker in schedule_item_speakers(self)
                    ],
                    conference_id=self.conference_id,
                )
            }

        for speaker in schedule_item_speakers(self):
            speakers.append(
                ScheduleItemUser(
                    id=speaker.id,
                    fullname=speaker.fullname,
                    full_name=speaker.full_name,
                    participant=Participant.from_model(participants_data[speaker.id])
                    if speaker.id in participants_data
                    else None,
                )
            )

        return speakers

    @strawberry.field
    def keynote(
        self, info: Info
    ) -> Annotated["Keynote", strawberry.lazy("api.conferences.types")] | None:
        if not self.keynote_id:
            return None

        return self.keynote

    @strawberry.field
    def rooms(self, info: Info) -> list[Room]:
        return self.rooms.all()

    @strawberry.field
    def image(self, info: Info) -> str | None:
        if not self.image:
            return None

        return info.context.request.build_absolute_uri(self.image.url)

    @strawberry.field(name="slidoUrl")
    def _slido_url(self, info: Info) -> str:
        if self.slido_url:
            return self.slido_url

        # For multi-room items we use the first room slido url
        return self.slot.day.added_rooms.get(room_id=self.rooms.first().id).slido_url
