from strawberry import LazyType
from typing import List, Optional

import strawberry
from api.languages.types import Language
from api.voting.types import VoteType
from voting.models import Vote

from datetime import datetime


from .permissions import CanSeeSubmissionDetail, CanSeeSubmissionPrivateFields


def restricted_field():
    """Field that can only be seen by admin, the submitter or who has the ticket
    until voting is not closed, after it will be public"""
    return strawberry.field(permission_classes=[CanSeeSubmissionDetail])


def private_field():
    """Field that can only be seen by admin and the submitter"""
    return strawberry.field(permission_classes=[CanSeeSubmissionPrivateFields])


@strawberry.type
class SubmissionType:
    id: strawberry.ID
    name: str


@strawberry.type
class SubmissionTag:
    id: strawberry.ID
    name: str


@strawberry.type
class SubmissionCommentAuthor:
    name: str


@strawberry.type
class SubmissionComment:
    id: strawberry.ID
    text: str
    created: datetime
    author: SubmissionCommentAuthor
    submission: LazyType["Submission", "api.submissions.types"]


@strawberry.type
class Submission:
    conference: LazyType["Conference", "api.conferences.types"]
    title: str
    slug: str
    elevator_pitch: Optional[str] = restricted_field()
    abstract: Optional[str] = restricted_field()
    speaker_level: Optional[str] = private_field()
    previous_talk_video: Optional[str] = private_field()
    notes: Optional[str] = private_field()
    speaker: Optional[LazyType["User", "api.users.types"]] = private_field()
    topic: Optional[LazyType["Topic", "api.conferences.types"]] = restricted_field()
    type: Optional[SubmissionType] = restricted_field()
    duration: Optional[
        LazyType["Duration", "api.conferences.types"]
    ] = restricted_field()
    audience_level: Optional[
        LazyType["AudienceLevel", "api.conferences.types"]
    ] = restricted_field()

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
            .select_related("author")
            .values("id", "text", "created", "author__id", "author__name")
        )

        return [
            SubmissionComment(
                id=comment["id"],
                text=comment["text"],
                created=comment["created"],
                submission=self,
                author=SubmissionCommentAuthor(
                    name="Speaker"
                    if comment["author__id"] == self.speaker.id
                    else comment["author__name"]
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
