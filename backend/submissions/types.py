import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from voting.models import Vote
from voting.types import VoteType

from .models import Submission
from .models import SubmissionType as ModelSubmissionType


class SubmissionTypeType(DjangoObjectType):
    class Meta:
        model = ModelSubmissionType
        only_fields = ("id", "name")


class SubmissionType(DjangoObjectType):
    votes = graphene.NonNull(graphene.List(VoteType))
    my_vote = graphene.Field(VoteType)

    def resolve_my_vote(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not logged in")

        try:
            return self.votes.get(user_id=info.context.user.id)
        except Vote.DoesNotExist:
            return None

    class Meta:
        model = Submission
        only_fields = (
            "id",
            "conference",
            "title",
            "elevator_pitch",
            "notes",
            "abstract",
            "owner",
            "helpers",
            "topic",
            "type",
            "duration",
        )
