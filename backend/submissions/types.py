from typing import TYPE_CHECKING, Optional

import strawberry
from graphql import GraphQLError
from voting.models import Vote
from voting.types import VoteType

if TYPE_CHECKING:  # pragma: no cover
    from conferences.types import Conference, Topic, Duration, AudienceLevel
    from users.types import User


@strawberry.type
class SubmissionType:
    id: strawberry.ID
    name: str


@strawberry.type
class Submission:
    id: strawberry.ID
    conference: "Conference"
    title: str
    elevator_pitch: str
    notes: str
    abstract: str
    speaker: "User"
    # helpers: str
    topic: "Topic"
    type: SubmissionType
    duration: "Duration"
    audience_level: "AudienceLevel"

    @strawberry.field
    def my_vote(self, info) -> Optional[VoteType]:
        request = info.context["request"]

        if not request.user.is_authenticated:
            raise GraphQLError("User not logged in")

        try:
            return self.votes.get(user_id=request.user.id)
        except Vote.DoesNotExist:
            return None
