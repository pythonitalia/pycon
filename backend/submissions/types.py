import graphene
from graphene_django import DjangoObjectType
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
    my_vote = graphene.Field(VoteType, user_id=graphene.ID())

    def resolve_my_vote(self, info, user_id):
        try:
            return self.votes.get(user_id=user_id)
        except Vote.DoesNotExist:
            return None

    def resolve_votes(self, info):
        return self.votes.all()

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
            "votes",
        )
