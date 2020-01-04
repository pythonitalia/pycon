from typing import TYPE_CHECKING, List, Optional

import strawberry
from api.languages.types import Language
from api.voting.types import VoteType
from graphql import GraphQLError
from strawberry.permission import BasePermission
from voting.models import Vote

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import Conference


class CanSeeSubmissionDetail(BasePermission):
    message = "You can't see details for this submission"

    def has_permission(self, source, info):
        user = info.context["request"].user

        # TODO: allow if they have tickets
        if not user.is_authenticated:
            return False

        return user.is_staff or source.speaker == user


def optional_field():
    """Field that can only be seen by admin and the submitter"""
    return strawberry.field(permission_classes=[CanSeeSubmissionDetail])


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
    elevator_pitch: Optional[str] = optional_field()
    notes: Optional[str] = optional_field()
    abstract: Optional[str] = optional_field()
    speaker_level: Optional[str] = optional_field()
    previous_talk_video: Optional[str] = optional_field()
    speaker: Optional["User"] = optional_field()
    topic: Optional["Topic"] = optional_field()
    type: Optional[SubmissionType] = optional_field()
    duration: Optional["Duration"] = optional_field()
    audience_level: Optional["AudienceLevel"] = optional_field()

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

    @strawberry.field(permission_classes=[CanSeeSubmissionDetail])
    def languages(self, info) -> Optional[List[Language]]:
        return self.languages.all()

    @strawberry.field(permission_classes=[CanSeeSubmissionDetail])
    def tags(self, info) -> Optional[List[SubmissionTag]]:
        return self.tags.all()
