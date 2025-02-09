from participants.models import Participant as ParticipantModel
from api.participants.types import Participant
import strawberry
from strawberry.types.field import StrawberryField
from strawberry.types import Info

from api.languages.types import Language
from api.voting.types import VoteType
from i18n.strings import LazyI18nString

from voting.models import Vote

from .permissions import CanSeeSubmissionPrivateFields, CanSeeSubmissionRestrictedFields
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from api.conferences.types import Conference, Topic, Duration, AudienceLevel
    from api.schedule.types import ScheduleItem


def private_field() -> StrawberryField:
    """Field that can only be seen by admin and the submitter"""

    def resolver(self, info: Info):
        if CanSeeSubmissionPrivateFields().has_permission(self, info):
            return getattr(self, info.python_name)
        return None

    return strawberry.field(resolver=resolver)


@strawberry.type
class SubmissionType:
    id: strawberry.ID
    name: str


@strawberry.type
class SubmissionTag:
    id: strawberry.ID
    name: str


@strawberry.type
class SubmissionSpeaker:
    id: strawberry.ID
    full_name: str
    gender: str


@strawberry.type
class MultiLingualString:
    it: str
    en: str

    @classmethod
    def create(cls, string: LazyI18nString):
        return cls(
            en=string.data.get("en", ""),
            it=string.data.get("it", ""),
        )


@strawberry.type
class ProposalMaterial:
    id: strawberry.ID
    name: str
    url: str | None
    file_url: str | None
    file_mime_type: str | None

    @classmethod
    def from_django(cls, material):
        return cls(
            id=material.id,
            name=material.name,
            url=material.url,
            file_url=material.file.url if material.file_id else None,
            file_mime_type=material.file.mime_type if material.file_id else None,
        )


@strawberry.type
class Submission:
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: str
    slug: str
    status: str
    speaker_level: str | None = private_field()
    previous_talk_video: str | None = private_field()
    short_social_summary: str | None = private_field()
    topic: Annotated["Topic", strawberry.lazy("api.conferences.types")] | None
    type: SubmissionType | None
    duration: Annotated["Duration", strawberry.lazy("api.conferences.types")] | None
    audience_level: Annotated[
        "AudienceLevel", strawberry.lazy("api.conferences.types")
    ] | None
    notes: str | None = private_field()

    @strawberry.field
    def schedule_items(
        self, info: Info
    ) -> list[Annotated["ScheduleItem", strawberry.lazy("api.schedule.types")]]:
        return self.schedule_items.all()

    @strawberry.field
    def multilingual_elevator_pitch(self, info: Info) -> MultiLingualString | None:
        return MultiLingualString.create(self.elevator_pitch)

    @strawberry.field
    def multilingual_abstract(self, info: Info) -> MultiLingualString | None:
        return MultiLingualString.create(self.abstract)

    @strawberry.field
    def multilingual_title(self, info: Info) -> MultiLingualString | None:
        return MultiLingualString.create(self.title)

    @strawberry.field
    def title(self, language: str) -> str:
        return self.title.localize(language)

    @strawberry.field()
    def elevator_pitch(self, language: str, info: Info) -> str | None:
        return self.elevator_pitch.localize(language)

    @strawberry.field()
    def abstract(self, language: str, info: Info) -> str | None:
        return self.abstract.localize(language)

    @strawberry.field
    def speaker(self, info: Info) -> Participant | None:
        if not CanSeeSubmissionRestrictedFields().has_permission(
            self, info, is_speaker_data=True
        ):
            return None

        participant = ParticipantModel.objects.filter(
            user_id=self.speaker_id, conference_id=self.conference_id
        ).first()
        return Participant.from_model(participant) if participant else None

    @strawberry.field
    def id(self, info) -> strawberry.ID:
        return self.hashid

    @strawberry.field
    def can_edit(self, info) -> bool:
        return self.can_edit(info.context.request)

    @strawberry.field
    def my_vote(self, info) -> VoteType | None:
        request = info.context.request

        if not request.user.is_authenticated:
            return None

        if info.context._my_votes is not None:
            return info.context._my_votes.get(self.id)

        try:
            return self.votes.get(user_id=request.user.id)
        except Vote.DoesNotExist:
            return None

    @strawberry.field
    def languages(self, info) -> list[Language] | None:
        return self.languages.all()

    @strawberry.field
    def tags(self, info) -> list[SubmissionTag] | None:
        return self.tags.all()

    @strawberry.field
    def materials(self, info) -> list[ProposalMaterial]:
        return [
            ProposalMaterial.from_django(material)
            for material in self.materials.order_by("created").all()
        ]


@strawberry.type
class SubmissionsPagination:
    submissions: list[Submission]
    total_pages: int
