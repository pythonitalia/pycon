import strawberry

from users.api.types import ScheduleItemUser, SubmissionSpeaker

from .mutation import Mutation
from .query import Query

schema = strawberry.federation.Schema(
    Query, Mutation, types=[ScheduleItemUser, SubmissionSpeaker]
)
