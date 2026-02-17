from typing import Annotated
from submissions.models import Submission as SubmissionModel

from files_upload.models import File
from api.utils import validate_url
from participants.models import Participant as ParticipantModel
import strawberry
from strawberry.types.field import StrawberryField
from strawberry.types import Info

from api.languages.types import Language
from api.voting.types import VoteType
from i18n.strings import LazyI18nString

from voting.models import Vote

from .permissions import CanSeeSubmissionPrivateFields, CanSeeSubmissionRestrictedFields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.conferences.types import Conference, Topic, Duration, AudienceLevel
    from api.schedule.types import ScheduleItem
    from api.participants.types import Participant
    from api.submissions.mutations import SendSubmissionErrors


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
    is_recordable: bool


@strawberry.type
class SubmissionTag:
    id: strawberry.ID
    name: str


@strawberry.type
class SubmissionSpeaker:
    id: strawberry.ID
    full_name: str
    gender: str
    _conference_id: strawberry.Private[str]

    @strawberry.field
    def participant(
        self, info: Info
    ) -> Annotated["Participant", strawberry.lazy("api.participants.types")] | None:
        from api.participants.types import Participant

        participant = (
            ParticipantModel.objects.for_conference(self._conference_id)
            .filter(user_id=self.id)
            .first()
        )
        return Participant.from_model(participant) if participant else None


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
    file_id: str | None
    file_url: str | None
    file_mime_type: str | None

    @classmethod
    def from_django(cls, material):
        return cls(
            id=material.id,
            name=material.name,
            url=material.url,
            file_id=material.file_id,
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
    audience_level: (
        Annotated["AudienceLevel", strawberry.lazy("api.conferences.types")] | None
    )
    notes: str | None = private_field()
    do_not_record: bool | None = private_field()

    @strawberry.field
    def schedule_items(
        self, info: Info
    ) -> list[Annotated["ScheduleItem", strawberry.lazy("api.schedule.types")]]:
        return self.schedule_items.all()

    @strawberry.field
    def has_schedule_items(self, info: Info) -> bool:
        return self.schedule_items.exists()

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
    def speaker(self, info: Info) -> SubmissionSpeaker | None:
        if not CanSeeSubmissionRestrictedFields().has_permission(
            self, info, is_speaker_data=True
        ):
            return None

        return SubmissionSpeaker(
            id=self.speaker_id,
            full_name=self.speaker.full_name,
            gender=self.speaker.gender,
            _conference_id=self.conference_id,
        )

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


@strawberry.input
class SubmissionMaterialInput:
    name: str
    id: strawberry.ID | None = None
    url: str | None = None
    file_id: str | None = None

    def validate(
        self, errors: "SendSubmissionErrors", submission: SubmissionModel
    ) -> "SendSubmissionErrors":
        if self.id:
            try:
                if not submission.materials.filter(id=int(self.id)).exists():
                    errors.add_error("id", "Material not found")
            except ValueError:
                errors.add_error("id", "Invalid material id")

        if self.file_id:
            if not File.objects.filter(
                id=self.file_id,
                uploaded_by_id=submission.speaker_id,
                type=File.Type.PROPOSAL_MATERIAL,
            ).exists():
                errors.add_error("file_id", "File not found")

        if self.url:
            if len(self.url) > 2048:
                errors.add_error("url", "URL is too long")
            elif not validate_url(self.url):
                errors.add_error("url", "Invalid URL")

        return errors
