from graphene import Enum
from graphene_django import DjangoObjectType

from .models import Vote


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        fields = ("id", "value", "user", "submission")


class VoteValues(Enum):
    NOT_INTERESTED = 0
    MAYBE = 1
    WANT_TO_SEE = 2
    MUST_SEE = 3
