import graphene

from .models import Conference
from .types import ConferenceType


class ConferenceQuery:
    conference = graphene.Field(ConferenceType, code=graphene.String())

    def resolve_conference(self, info, code):
        return Conference.objects.get(code=code)
