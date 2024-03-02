from api.context import Info
from api.participants.types import Participant
from participants.models import Participant as ParticipantModel
from typing import TYPE_CHECKING
from api.languages.types import Language
from datetime import datetime
from typing import Annotated
from api.schedule.types.schedule_item_user import ScheduleItemUser
from api.submissions.types import Submission
import strawberry
from api.schedule.types.room import Room

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import AudienceLevel, Conference, Keynote


@strawberry.type
class ScheduleItem:
    id: strawberry.ID
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: str
    start: datetime
    end: datetime
    status: str
    submission: Submission | None
    slug: str
    description: str
    type: str
    duration: int | None
    highlight_color: str | None
    language: Language
    audience_level: Annotated[
        "AudienceLevel", strawberry.lazy("api.conferences.types")
    ] | None
    youtube_video_id: str | None

    @strawberry.field
    def abstract(self) -> str:
        if self.submission_id:
            return self.submission.abstract.localize(self.language.code)

        return ""

    @strawberry.field
    def elevator_pitch(self) -> str:
        if self.submission_id:
            return self.submission.elevator_pitch.localize(self.language.code)

        return ""

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
    def speakers(self, info: Info) -> list[ScheduleItemUser]:
        speakers = []

        # TODO: Find a better solution
        participants_data = info.context._participants_data
        if not participants_data:
            participants_data = {
                participant.user_id: participant
                for participant in ParticipantModel.objects.filter(
                    user_id__in=[speaker.id for speaker in self.speakers],
                    conference_id=self.conference_id,
                )
            }

        for speaker in self.speakers:
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
        from api.conferences.types import Keynote

        if not self.keynote_id:
            return None

        return Keynote.from_django_model(self.keynote, info)

    @strawberry.field
    def rooms(self, info) -> list[Room]:
        return self.rooms.all()

    @strawberry.field
    def image(self, info) -> str | None:
        if not self.image:
            return None

        return info.context.request.build_absolute_uri(self.image.url)

    @strawberry.field
    def slido_url(self, info) -> str:
        if self.slido_url:
            return self.slido_url

        # For multi-room items we use the first room slido url
        return self.slot.day.added_rooms.get(room_id=self.rooms.first().id).slido_url
