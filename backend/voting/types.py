from graphene_django import DjangoObjectType
from voting.models import VoteRange, Vote


class VoteRangeType(DjangoObjectType):
    class Meta:
        model = VoteRange
        only_fields = (
            'name',
            'first',
            'last',
            'step',
        )


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        only_fields = (
            'id',
            'range',
            'value',
            'user',
            'submission'
        )
