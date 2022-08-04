from datetime import datetime
from typing import List, Optional

import strawberry
from strawberry import LazyType
from strawberry.field import StrawberryField
from strawberry.types import Info

from api.languages.types import Language
from api.voting.types import VoteType
from i18n.strings import LazyI18nString
from voting.models import Vote

from .permissions import CanSeeSubmissionPrivateFields, CanSeeSubmissionRestrictedFields


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


@strawberry.federation.type(keys=["id"])
class SubmissionCommentAuthor:
    id: strawberry.ID
    is_speaker: bool


@strawberry.type
class SubmissionComment:
    id: strawberry.ID
    text: str
    created: datetime
    author: SubmissionCommentAuthor
    submission: LazyType["Submission", "api.submissions.types"]


@strawberry.federation.type(keys=["id"])
class SubmissionSpeaker:
    id: strawberry.ID


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
    conference: LazyType["Conference", "api.conferences.types"]
    title: str
    slug: str
    status: str
    speaker_level: Optional[str] = private_field()
    previous_talk_video: Optional[str] = private_field()
    topic: Optional[LazyType["Topic", "api.conferences.types"]] = restricted_field()
    type: Optional[SubmissionType] = restricted_field()
    duration: Optional[
        LazyType["Duration", "api.conferences.types"]
    ] = restricted_field()
    audience_level: Optional[
        LazyType["AudienceLevel", "api.conferences.types"]
    ] = restricted_field()
    notes: Optional[str] = private_field()

    @restricted_field()
    def multilingual_elevator_pitch(self) -> Optional[MultiLingualString]:
        return MultiLingualString.create(self.elevator_pitch)

    @restricted_field()
    def multilingual_abstract(self) -> Optional[MultiLingualString]:
        return MultiLingualString.create(self.abstract)

    @restricted_field()
    def multilingual_title(self) -> Optional[MultiLingualString]:
        return MultiLingualString.create(self.title)

    @strawberry.field
    def title(self, language: str) -> str:
        return self.title.localize(language)

    @restricted_field()
    def elevator_pitch(self, language: str) -> Optional[str]:
        return self.elevator_pitch.localize(language)

    @restricted_field()
    def abstract(self, language: str) -> Optional[str]:
        return self.abstract.localize(language)

    @strawberry.field
    def speaker(self, info) -> Optional[SubmissionSpeaker]:
        if CanSeeSubmissionRestrictedFields().has_permission(self, info):
            return SubmissionSpeaker(id=self.speaker_id)
        return None

    @strawberry.field
    def id(self, info) -> strawberry.ID:
        return self.hashid

    @strawberry.field
    def can_edit(self, info) -> bool:
        return self.can_edit(info.context.request)

    @strawberry.field(permission_classes=[CanSeeSubmissionRestrictedFields])
    def comments(self, info) -> List[SubmissionComment]:
        comments = (
            self.comments.all()
            .order_by("created")
            .values("id", "text", "created", "author_id", "submission__speaker_id")
        )

        return [
            SubmissionComment(
                id=comment["id"],
                text=comment["text"],
                created=comment["created"],
                submission=self,
                author=SubmissionCommentAuthor(
                    id=comment["author_id"],
                    is_speaker=comment["author_id"]
                    == comment["submission__speaker_id"],
                ),
            )
            for comment in comments
        ]

    @strawberry.field
    def my_vote(self, info) -> Optional[VoteType]:
        request = info.context.request

        if not request.pastaporto.is_authenticated:
            return None

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
