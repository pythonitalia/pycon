from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django
from strawberry.types import Info
from strawberry.types.field import StrawberryField

from api.languages.types import Language
from api.utils import validate_url
from api.voting.types import VoteType
from files_upload import models as file_models
from i18n.strings import LazyI18nString
from participants import models as participant_models
from submissions import models
from voting import models as voting_models

from .permissions import CanSeeSubmissionPrivateFields, CanSeeSubmissionRestrictedFields

if TYPE_CHECKING:
    from api.conferences.types import AudienceLevel, Conference, Duration, Topic
    from api.participants.types import Participant
    from api.schedule.types import ScheduleItem
    from api.submissions.mutations import SendSubmissionErrors


def private_field(name: str) -> StrawberryField:
    """Field that can only be seen by admin and the submitter"""

    def resolver(self, info: Info):
        if CanSeeSubmissionPrivateFields().has_permission(self, info):
            return getattr(self, info.python_name)
        return None

    return strawberry_django.field(resolver=resolver, only=[name])


@strawberry_django.type(models.SubmissionType)
class SubmissionType:
    id: strawberry.auto
    name: strawberry.auto
    is_recordable: strawberry.auto


@strawberry_django.type(models.SubmissionTag)
class SubmissionTag:
    id: strawberry.auto
    name: strawberry.auto


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
            participant_models.Participant.objects.for_conference(self._conference_id)
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


@strawberry_django.type(models.Submission)
class Submission:
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: str
    slug: strawberry.auto
    status: strawberry.auto
    speaker_level: str | None = private_field("speaker_level")
    previous_talk_video: str | None = private_field("previous_talk_video")
    short_social_summary: str | None = private_field("short_social_summary")
    topic: Annotated["Topic", strawberry.lazy("api.conferences.types")] | None
    type: SubmissionType | None
    duration: Annotated["Duration", strawberry.lazy("api.conferences.types")] | None
    audience_level: (
        Annotated["AudienceLevel", strawberry.lazy("api.conferences.types")] | None
    )
    notes: str | None = private_field("notes")
    do_not_record: bool | None = private_field("do_not_record")

    schedule_items: list[
        Annotated["ScheduleItem", strawberry.lazy("api.schedule.types")]
    ]

    @strawberry_django.field(only=["elevator_pitch"])
    def multilingual_elevator_pitch(self, info: Info) -> MultiLingualString | None:
        return MultiLingualString.create(self.elevator_pitch)

    @strawberry_django.field(only=["abstract"])
    def multilingual_abstract(self, info: Info) -> MultiLingualString | None:
        return MultiLingualString.create(self.abstract)

    @strawberry_django.field(only=["title"])
    def multilingual_title(self, info: Info) -> MultiLingualString | None:
        return MultiLingualString.create(self.title)

    @strawberry_django.field(only=["title"])
    def title(self, language: str) -> str:
        return self.title.localize(language)

    @strawberry_django.field(only=["elevator_pitch"])
    def elevator_pitch(self, language: str, info: Info) -> str | None:
        return self.elevator_pitch.localize(language)

    @strawberry_django.field(only=["abstract"])
    def abstract(self, language: str, info: Info) -> str | None:
        return self.abstract.localize(language)

    @strawberry_django.field(
        only=["conference_id"],
        select_related=["speaker"],
    )
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

    @strawberry_django.field(only=["id"])
    def id(self, info: Info) -> strawberry.ID:
        return self.hashid

    @strawberry_django.field(only=["speaker_id"])
    def can_edit(self, info: Info) -> bool:
        return self.can_edit(info.context.request)

    @strawberry.field
    def my_vote(self, info: Info) -> VoteType | None:
        request = info.context.request

        if not request.user.is_authenticated:
            return None

        if info.context._my_votes is not None:
            return info.context._my_votes.get(self.id)

        try:
            return self.votes.get(user_id=request.user.id)
        except voting_models.Vote.DoesNotExist:
            return None

    @strawberry_django.field
    def languages(self, info: Info) -> list[Language] | None:
        return self.languages.all()

    @strawberry_django.field
    def tags(self, info: Info) -> list[SubmissionTag] | None:
        return self.tags.all()

    @strawberry.field
    def materials(self, info: Info) -> list[ProposalMaterial]:
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
        self, errors: "SendSubmissionErrors", submission: models.Submission
    ) -> "SendSubmissionErrors":
        if self.id:
            try:
                if not submission.materials.filter(id=int(self.id)).exists():
                    errors.add_error("id", "Material not found")
            except ValueError:
                errors.add_error("id", "Invalid material id")

        if (
            self.file_id
            and not file_models.File.objects.filter(
                id=self.file_id,
                uploaded_by_id=submission.speaker_id,
                type=file_models.File.Type.PROPOSAL_MATERIAL,
            ).exists()
        ):
            errors.add_error("file_id", "File not found")

        if self.url:
            if len(self.url) > 2048:
                errors.add_error("url", "URL is too long")
            elif not validate_url(self.url):
                errors.add_error("url", "Invalid URL")

        return errors
