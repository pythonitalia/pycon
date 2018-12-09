import graphene

from graphene_django import DjangoObjectType

from tickets.types import TicketType
from languages.types import LanguageType

from .models import Conference, Deadline, AudienceLevel, Topic, Duration


class DurationType(DjangoObjectType):
    class Meta:
        model = Duration
        only_fields = (
            'id',
            'conference',
            'name',
            'duration',
            'notes',
        )


class DeadlineModelType(DjangoObjectType):
    class Meta:
        model = Deadline
        only_fields = (
            'conference',
            'type',
            'name',
            'start',
            'end',
        )


class AudienceLevelType(DjangoObjectType):
    class Meta:
        model = AudienceLevel
        only_fields = ('id', 'name', )


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        only_fields = ('id', 'name')


class ConferenceType(DjangoObjectType):
    tickets = graphene.NonNull(graphene.List(graphene.NonNull(TicketType)))
    deadlines = graphene.NonNull(graphene.List(graphene.NonNull(DeadlineModelType)))
    audience_levels = graphene.NonNull(graphene.List(graphene.NonNull(AudienceLevelType)))
    topics = graphene.NonNull(graphene.List(graphene.NonNull(TopicType)))
    languages = graphene.NonNull(graphene.List(graphene.NonNull(LanguageType)))
    durations = graphene.NonNull(graphene.List(graphene.NonNull(DurationType)))

    def resolve_tickets(self, info):
        return self.tickets.all()

    def resolve_deadlines(self, info):
        return self.deadlines.order_by('start').all()

    def resolve_audience_levels(self, info):
        return self.audience_levels.all()

    def resolve_topics(self, info):
        return self.topics.all()

    def resolve_languages(self, info):
        return self.languages.all()

    def resolve_durations(self, info):
        return self.durations.all()

    class Meta:
        model = Conference
        only_fields = (
            'id',
            'name',
            'code',
            'start',
            'end',
            'deadlines',
            'audience_levels',
            'topics',
            'languages',
            'durations',
        )
