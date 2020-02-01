from datetime import datetime
from itertools import groupby
from typing import List, Optional

import pytz
import strawberry
from api.cms.types import FAQ, Menu
from api.events.types import Event
from api.hotels.types import HotelRoom
from api.languages.types import Language
from api.pretix.query import get_conference_tickets
from api.pretix.types import TicketItem
from api.scalars import Date, DateTime
from api.schedule.types import Room, ScheduleItem
from api.sponsors.types import SponsorsByLevel
from api.submissions.types import Submission, SubmissionType
from api.voting.types import RankSubmission
from cms.models import GenericCopy
from django.conf import settings
from django.utils import translation
from schedule.models import ScheduleItem as ScheduleItemModel
from voting.models import RankRequest as RankRequestModel

from ..helpers.i18n import make_localized_resolver
from ..helpers.maps import Map, resolve_map
from ..permissions import CanSeeSubmissions


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

    pretix_event_url: str

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
    def tickets(self, info, language: str) -> List[TicketItem]:
        return get_conference_tickets(self, language=language)

    @strawberry.field
    def hotel_rooms(self, info) -> List[HotelRoom]:
        return self.hotel_rooms.all()

    @strawberry.field
    def deadlines(self, info) -> List["Deadline"]:
        return self.deadlines.order_by("start").all()

    @strawberry.field(name="isCFPOpen")
    def is_cfp_open(self, info) -> bool:
        return self.is_cfp_open

    @strawberry.field
    def is_voting_open(self, info) -> bool:
        return self.is_voting_open

    @strawberry.field
    def deadline(self, info, type: str) -> Optional["Deadline"]:
        return self.deadlines.filter(type=type).first()

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
    def submission_types(self, info) -> List[SubmissionType]:
        return self.submission_types.all()

    @strawberry.field(permission_classes=[CanSeeSubmissions])
    def submissions(self, info) -> Optional[List[Submission]]:
        return self.submissions.all().select_related(
            "audience_level", "duration", "type", "topic"
        )

    @strawberry.field
    def events(self, info) -> List[Event]:
        return self.events.all()

    @strawberry.field
    def rooms(self, info) -> List[Room]:
        return self.rooms.all()

    @strawberry.field
    def faqs(self, info) -> List[FAQ]:
        return self.faqs.all()

    @strawberry.field
    def sponsors_by_level(self, info) -> List[SponsorsByLevel]:
        from sponsors.models import Sponsor

        sponsors = Sponsor.objects.filter(
            level__conference__code=self.code
        ).select_related("level")

        by_level = groupby(sponsors, key=lambda sponsor: sponsor.level)

        return [
            SponsorsByLevel(level.name, list(sponsors), level.highlight_color)
            for level, sponsors in by_level
        ]

    @strawberry.field
    def copy(self, info, key: str, language: Optional[str] = None) -> Optional[str]:
        copy = GenericCopy.objects.filter(conference=self, key=key).first()

        language = language or translation.get_language() or settings.LANGUAGE_CODE

        return copy.content.localize(language) if copy else None

    @strawberry.field
    def menu(self, info, identifier: str) -> Optional[Menu]:
        return (
            self.menus.filter(identifier=identifier).prefetch_related("links").first()
        )

    @strawberry.field
    def keynotes(self, info) -> List[ScheduleItem]:
        return self.schedule_items.filter(type=ScheduleItemModel.TYPES.keynote).all()

    @strawberry.field
    def talk(self, info, slug: str) -> Optional[ScheduleItem]:
        return self.schedule_items.filter(slug=slug).first()

    @strawberry.field
    def ranking(self, info) -> List[RankSubmission]:
        return (
            RankRequestModel.objects.filter(conference=self)
            .last()
            .rank_submissions.all()
            .order_by("absolute_rank")
        )


@strawberry.type
class Deadline:
    type: str
    name: str = strawberry.field(resolver=make_localized_resolver("name"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    start: DateTime
    end: DateTime
    conference: Conference


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
