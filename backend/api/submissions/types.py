from typing import TYPE_CHECKING, List, Optional

import strawberry
from graphql import GraphQLError

from api.languages.types import Language
from api.voting.types import VoteType
from voting.models import Vote

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import Conference, Topic, Duration, AudienceLevel
    from api.users.types import User


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
    id: strawberry.ID
    conference: "Conference"
    title: str
    slug: str
    elevator_pitch: str
    notes: str
    abstract: str
    speaker: "User"
    topic: "Topic"
    type: SubmissionType
    duration: "Duration"
    audience_level: "AudienceLevel"
    languages: List["Language"]

    @strawberry.field
    def my_vote(self, info) -> Optional[VoteType]:
        request = info.context["request"]

        if not request.user.is_authenticated:
            raise GraphQLError("User not logged in")

        try:
            return self.votes.get(user_id=request.user.id)
        except Vote.DoesNotExist:
            return None

    @strawberry.field
    def languages(self, info) -> List[Language]:
        return self.languages.all()

    @strawberry.field
    def tags(self, info) -> List[SubmissionTag]:
        return self.tags.all()
