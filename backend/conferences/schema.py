import graphene

from .types import ConferenceType
from .models import Conference


class ConferenceQuery(graphene.AbstractType):
    conference = graphene.Field(ConferenceType, slug=graphene.String())

    def resolve_conference(self, info, slug):
        return Conference.objects.get(slug=slug)
