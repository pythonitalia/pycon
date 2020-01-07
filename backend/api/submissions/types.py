from typing import TYPE_CHECKING, List, Optional

import strawberry
from api.languages.types import Language
from api.voting.types import VoteType
from graphql import GraphQLError
from voting.models import Vote

from .permissions import CanSeeSubmissionPrivateFields, CanSeeSubmissionTicketDetail

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import Conference


def ticket_only_field():
    """Field that can only be seen by admin, the submitter or who has the ticket"""
    return strawberry.field(permission_classes=[CanSeeSubmissionTicketDetail])


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
class Submission:
    conference: "Conference"
    title: str
    slug: str
    elevator_pitch: Optional[str] = ticket_only_field()
    notes: Optional[str] = ticket_only_field()
    abstract: Optional[str] = ticket_only_field()
    speaker_level: Optional[str] = private_field()
    previous_talk_video: Optional[str] = private_field()
    speaker: Optional["User"] = private_field()
    topic: Optional["Topic"] = ticket_only_field()
    type: Optional[SubmissionType] = ticket_only_field()
    duration: Optional["Duration"] = ticket_only_field()
    audience_level: Optional["AudienceLevel"] = ticket_only_field()

    @strawberry.field
    def id(self, info) -> strawberry.ID:
        return self.hashid

    @strawberry.field
    def can_edit(self, info) -> bool:
        return self.can_edit(info.context["request"])

    @strawberry.field
    def my_vote(self, info) -> Optional[VoteType]:
        request = info.context["request"]

        if not request.user.is_authenticated:
            raise GraphQLError("User not logged in")

        try:
            return self.votes.get(user_id=request.user.id)
        except Vote.DoesNotExist:
            return None

    @strawberry.field(permission_classes=[CanSeeSubmissionTicketDetail])
    def languages(self, info) -> Optional[List[Language]]:
        return self.languages.all()

    @strawberry.field(permission_classes=[CanSeeSubmissionTicketDetail])
    def tags(self, info) -> Optional[List[SubmissionTag]]:
        return self.tags.all()
