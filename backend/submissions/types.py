from graphene_django import DjangoObjectType

from .models import Submission


class ModelSubmissionType(DjangoObjectType):
    class Meta:
        model = Submission
        only_fields = (
            'id',
            'conference',
            'title',
            'abstract',
            'owner',
            'helpers',
            'topic',
            'type',
        )
