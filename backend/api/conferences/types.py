from datetime import datetime
from itertools import groupby
from typing import TYPE_CHECKING, List, Optional

import pytz
import strawberry
from api.events.types import Event
from api.languages.types import Language
from api.scalars import Date, DateTime
from api.schedule.types import Room, ScheduleItem
from api.sponsors.types import SponsorsByLevel
from api.submissions.types import Submission, SubmissionType
from cms.models import GenericCopy
from django.conf import settings
from django.utils import translation

from ..helpers.i18n import make_localized_resolver
from ..helpers.maps import Map, resolve_map

if TYPE_CHECKING:  # pragma: no cover
    from api.tickets.types import TicketQuestion


@strawberry.type
class AudienceLevel:
    id: strawberry.ID
    name: str


@strawberry.type
class Topic:
    id: strawberry.ID
    name: str


@strawberry.type
class Conference:
    id: strawberry.ID

    name: str = strawberry.field(resolver=make_localized_resolver("name"))
    introduction: str = strawberry.field(
        resolver=make_localized_resolver("introduction")
    )
    code: str
    start: DateTime
    end: DateTime
    map: Optional[Map] = strawberry.field(resolver=resolve_map)

    @strawberry.field
    def timezone(self, info) -> str:
        return str(self.timezone)

    @strawberry.field
    def schedule(self, info, date: Date = None) -> List[ScheduleItem]:
        qs = self.schedule_items

        if date:
            start_date = datetime.combine(date, datetime.min.time())
            end_date = datetime.combine(date, datetime.max.time())

            utc_start_date = pytz.utc.normalize(start_date.astimezone(pytz.utc))
            utc_end_date = pytz.utc.normalize(end_date.astimezone(pytz.utc))

            qs = qs.filter(start__gte=utc_start_date, end__lte=utc_end_date)

        return qs.order_by("start")

    @strawberry.field
    def ticket_fares(self, info) -> List["TicketFare"]:
        return self.ticket_fares.all()

    @strawberry.field
    def deadlines(self, info) -> List["Deadline"]:
        return self.deadlines.order_by("start").all()

    @strawberry.field
    def audience_levels(self, info) -> List[AudienceLevel]:
        return self.audience_levels.all()

    @strawberry.field
    def topics(self, info) -> List[Topic]:
        return self.topics.all()

    @strawberry.field
    def languages(self, info) -> List[Language]:
        return self.languages.all()

    @strawberry.field
    def durations(self, info) -> List["Duration"]:
        return self.durations.all()

    @strawberry.field
    def submissions(self, info) -> List[Submission]:
        return self.submissions.all()

    @strawberry.field
    def events(self, info) -> List[Event]:
        return self.events.all()

    @strawberry.field
    def rooms(self, info) -> List[Room]:
        return self.rooms.all()

    @strawberry.field
    def sponsors_by_level(self, info) -> List[SponsorsByLevel]:
        from sponsors.models import Sponsor

        sponsors = Sponsor.objects.filter(
            level__conference__code=self.code
        ).select_related("level")

        by_level = groupby(sponsors, key=lambda sponsor: sponsor.level.name)

        return [SponsorsByLevel(level, list(sponsors)) for level, sponsors in by_level]

    @strawberry.field
    def copy(self, info, key: str, language: Optional[str] = None) -> Optional[str]:
        copy = GenericCopy.objects.filter(conference=self, key=key).first()

        language = language or translation.get_language() or settings.LANGUAGE_CODE

        return copy.content.localize(language) if copy else None


@strawberry.type
class Deadline:
    type: str
    name: str
    start: DateTime
    end: DateTime
    conference: Conference


@strawberry.type
class TicketFareQuestion:
    ticket_fare: "TicketFare"
    question: "TicketQuestion"
    is_required: bool


@strawberry.type
class TicketFare:
    id: strawberry.ID
    code: str
    name: str
    price: str
    start: DateTime
    end: DateTime
    description: str
    conference: Conference

    @strawberry.field
    def questions(self, info) -> List["TicketFareQuestion"]:
        return self.questions.all()


@strawberry.type
class Duration:
    id: strawberry.ID
    conference: Conference
    name: str
    duration: int
    notes: str

    @strawberry.field
    def allowed_submission_types(self, info) -> List[SubmissionType]:
        return self.allowed_submission_types.all()
