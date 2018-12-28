from graphene_django import DjangoObjectType

from .models import Submission, SubmissionType as ModelSubmissionType


class SubmissionTypeType(DjangoObjectType):
    class Meta:
        model = ModelSubmissionType
        only_fields = (
            'id',
            'name'
        )


class SubmissionType(DjangoObjectType):
    class Meta:
        model = Submission
        only_fields = (
            'id',
            'conference',
            'title',
            'elevator_pitch',
            'notes',
            'abstract',
            'owner',
            'helpers',
            'topic',
            'type',
            'duration',
        )
