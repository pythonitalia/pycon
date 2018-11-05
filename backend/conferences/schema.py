import graphene

from .types import ConferenceType
from .models import Conference


class ConferenceQuery(graphene.AbstractType):
    conference = graphene.Field(ConferenceType, code=graphene.String())

    def resolve_conference(self, info, code):
        return Conference.objects.get(code=code)
