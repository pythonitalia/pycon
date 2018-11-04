from graphene_django import DjangoObjectType

from .models import Talk


class TalkType(DjangoObjectType):
    class Meta:
        model = Talk
        only_fields = (
            'conference',
            'title',
            'abstract',
            'owner',
            'helpers',
            'topic'
        )
