from typing import List, Optional

import strawberry
from strawberry.field import StrawberryField
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


def restricted_field() -> StrawberryField:
    """Field that can only be seen by admin, the submitter or who has the ticket
    until voting is not closed, after it will be public"""

    def resolver(self, info: Info):
        if CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return getattr(self, info.python_name)
        return None

    return strawberry.field(resolver=resolver)


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
class Submission:
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: str
    slug: str
    status: str
    speaker_level: Optional[str] = private_field()
    previous_talk_video: Optional[str] = private_field()
    short_social_summary: Optional[str] = private_field()
    topic: Optional[
        Annotated["Topic", strawberry.lazy("api.conferences.types")]
    ] = restricted_field()
    type: Optional[SubmissionType] = restricted_field()
    duration: Optional[
        Annotated["Duration", strawberry.lazy("api.conferences.types")]
    ] = restricted_field()
    audience_level: Optional[
        Annotated["AudienceLevel", strawberry.lazy("api.conferences.types")]
    ] = restricted_field()
    notes: Optional[str] = private_field()

    @strawberry.field
    def schedule_items(
        self, info: Info
    ) -> List[Annotated["ScheduleItem", strawberry.lazy("api.schedule.types")]]:
        return self.schedule_items.all()

    @strawberry.field
    def multilingual_elevator_pitch(self, info: Info) -> Optional[MultiLingualString]:
        if not CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return None
        return MultiLingualString.create(self.elevator_pitch)

    @strawberry.field
    def multilingual_abstract(self, info: Info) -> Optional[MultiLingualString]:
        if not CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return None

        return MultiLingualString.create(self.abstract)

    @strawberry.field
    def multilingual_title(self, info: Info) -> Optional[MultiLingualString]:
        if not CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return None

        return MultiLingualString.create(self.title)

    @strawberry.field
    def title(self, language: str) -> str:
        return self.title.localize(language)

    @strawberry.field()
    def elevator_pitch(self, language: str, info: Info) -> Optional[str]:
        if not CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return None

        return self.elevator_pitch.localize(language)

    @strawberry.field()
    def abstract(self, language: str, info: Info) -> Optional[str]:
        if not CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return None

        return self.abstract.localize(language)

    @strawberry.field
    def speaker(self, info: Info) -> Optional[SubmissionSpeaker]:
        if not CanSeeSubmissionRestrictedFields().has_permission(
            self, info, is_speaker_data=True
        ):
            return None

        return SubmissionSpeaker(
            id=self.speaker_id,
            full_name=self.speaker.full_name,
            gender=self.speaker.gender,
        )

    @strawberry.field
    def id(self, info) -> strawberry.ID:
        return self.hashid

    @strawberry.field
    def can_edit(self, info) -> bool:
        return self.can_edit(info.context.request)

    @strawberry.field
    def my_vote(self, info) -> Optional[VoteType]:
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
    def languages(self, info) -> Optional[List[Language]]:
        if CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return self.languages.all()
        return None

    @strawberry.field
    def tags(self, info) -> Optional[List[SubmissionTag]]:
        if CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return self.tags.all()
        return None


@strawberry.type
class SubmissionsPagination:
    submissions: List[Submission]
    total_pages: int
