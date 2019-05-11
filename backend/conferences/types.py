from datetime import datetime

import graphene
from graphene_django import DjangoObjectType

import pytz

from languages.types import LanguageType
from schedule.types import ModelScheduleItemType
from submissions.types import SubmissionTypeType

from .models import AudienceLevel, Conference, Deadline, Duration, Ticket, Topic


class DurationType(DjangoObjectType):
    allowed_submission_types = graphene.NonNull(
        graphene.List(graphene.NonNull(SubmissionTypeType))
    )

    def resolve_allowed_submission_types(self, info):
        return self.allowed_submission_types.all()

    class Meta:
        model = Duration
        only_fields = (
            "id",
            "conference",
            "name",
            "duration",
            "notes",
            "allowed_submission_types",
        )


class DeadlineModelType(DjangoObjectType):
    class Meta:
        model = Deadline
        only_fields = ("conference", "type", "name", "start", "end")


class AudienceLevelType(DjangoObjectType):
    class Meta:
        model = AudienceLevel
        only_fields = ("id", "name")


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        only_fields = ("id", "name")


class TicketType(DjangoObjectType):
    class Meta:
        model = Ticket
        only_fields = ("id", "code", "name", "price", "start", "end", "description")


class ConferenceType(DjangoObjectType):
    tickets = graphene.NonNull(graphene.List(graphene.NonNull(TicketType)))
    deadlines = graphene.NonNull(graphene.List(graphene.NonNull(DeadlineModelType)))
    audience_levels = graphene.NonNull(
        graphene.List(graphene.NonNull(AudienceLevelType))
    )
    topics = graphene.NonNull(graphene.List(graphene.NonNull(TopicType)))
    languages = graphene.NonNull(graphene.List(graphene.NonNull(LanguageType)))
    durations = graphene.NonNull(graphene.List(graphene.NonNull(DurationType)))
    schedule = graphene.NonNull(
        graphene.List(graphene.NonNull(ModelScheduleItemType)), date=graphene.Date()
    )

    timezone = graphene.String()

    def resolve_timezone(self, info):
        return str(self.timezone)

    def resolve_schedule(self, info, date=None):
        qs = self.schedule_items

        if date:
            start_date = datetime.combine(date, datetime.min.time())
            end_date = datetime.combine(date, datetime.max.time())

            utc_start_date = pytz.utc.normalize(start_date.astimezone(pytz.utc))
            utc_end_date = pytz.utc.normalize(end_date.astimezone(pytz.utc))

            qs = qs.filter(start__gte=utc_start_date, end__lte=utc_end_date)

        return qs.order_by("start")

    def resolve_tickets(self, info):
        return self.tickets.all()

    def resolve_deadlines(self, info):
        return self.deadlines.order_by("start").all()

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
            "id",
            "name",
            "code",
            "start",
            "end",
            "deadlines",
            "audience_levels",
            "topics",
            "languages",
            "durations",
            "timezone",
            "rooms",
        )
