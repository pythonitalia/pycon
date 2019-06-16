import graphene
from graphene_django import DjangoObjectType

from voting.types import VoteType

from .models import Submission
from .models import SubmissionType as ModelSubmissionType


class SubmissionTypeType(DjangoObjectType):
    class Meta:
        model = ModelSubmissionType
        only_fields = ("id", "name")


class SubmissionType(DjangoObjectType):
    votes = graphene.NonNull(graphene.List(graphene.NonNull(VoteType)))

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
