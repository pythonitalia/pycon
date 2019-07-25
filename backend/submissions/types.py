from typing import Optional

import strawberry
from graphql import GraphQLError
from voting.models import Vote
from voting.types import VoteType

if False:
    from conferences.types import Conference, Topic, Duration
    from users.types import UserType


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
    speaker: "UserType"
    # helpers: str
    topic: "Topic"
    type: SubmissionType
    duration: "Duration"

    @strawberry.field
    def my_vote(self, info) -> Optional[VoteType]:
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not logged in")

        try:
            return self.votes.get(user_id=info.context.user.id)
        except Vote.DoesNotExist:
            return None
