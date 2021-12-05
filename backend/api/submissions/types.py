from datetime import datetime
from typing import List, Optional

import strawberry
from strawberry import LazyType

from api.languages.types import Language
from api.voting.types import VoteType
from voting.models import Vote

from .permissions import CanSeeSubmissionDetail, CanSeeSubmissionPrivateFields


def restricted_field(field_name):
    """Field that can only be seen by admin, the submitter or who has the ticket
    until voting is not closed, after it will be public"""

    def resolver(self, info):
        if CanSeeSubmissionDetail().has_permission(self, info):
            return getattr(self, field_name)
        return None

    return strawberry.field(resolver=resolver)


def private_field(field_name):
    """Field that can only be seen by admin and the submitter"""

    def resolver(self, info):
        if CanSeeSubmissionPrivateFields().has_permission(self, info):
            return getattr(self, field_name)
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
class Submission:
    conference: LazyType["Conference", "api.conferences.types"]
    title: str
    slug: str
    elevator_pitch: Optional[str] = restricted_field("elevator_pitch")
    abstract: Optional[str] = restricted_field("abstract")
    speaker_level: Optional[str] = private_field("speaker_level")
    previous_talk_video: Optional[str] = private_field("previous_talk_video")
    topic: Optional[LazyType["Topic", "api.conferences.types"]] = restricted_field(
        "topic"
    )
    type: Optional[SubmissionType] = restricted_field("type")
    duration: Optional[
        LazyType["Duration", "api.conferences.types"]
    ] = restricted_field("duration")
    audience_level: Optional[
        LazyType["AudienceLevel", "api.conferences.types"]
    ] = restricted_field("audience_level")
    notes: Optional[str] = private_field("notes")

    @strawberry.field(permission_classes=[CanSeeSubmissionPrivateFields])
    def speaker(self) -> SubmissionSpeaker:
        return SubmissionSpeaker(id=self.speaker_id)

    @strawberry.field
    def id(self, info) -> strawberry.ID:
        return self.hashid

    @strawberry.field
    def can_edit(self, info) -> bool:
        return self.can_edit(info.context.request)

    @strawberry.field(permission_classes=[CanSeeSubmissionDetail])
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

        try:
            return self.votes.get(user_id=request.user.id)
        except Vote.DoesNotExist:
            return None

    @strawberry.field(permission_classes=[CanSeeSubmissionDetail])
    def languages(self, info) -> Optional[List[Language]]:
        return self.languages.all()

    @strawberry.field(permission_classes=[CanSeeSubmissionDetail])
    def tags(self, info) -> Optional[List[SubmissionTag]]:
        return self.tags.all()
