from datetime import datetime
from decimal import Decimal
from itertools import groupby
from typing import List, Optional

import pytz
import strawberry
from api.scalars import Date, DateTime
from cms.models import GenericCopy
from languages.types import Language
from schedule.types import Room, ScheduleItem
from sponsors.types import SponsorsByLevel
from submissions.types import Submission, SubmissionType

from .helpers.maps import generate_map_image


@strawberry.type
class AudienceLevel:
    id: strawberry.ID
    name: str


@strawberry.type
class Topic:
    id: strawberry.ID
    name: str


@strawberry.type
class Map:
    latitude: Decimal
    longitude: Decimal
    link: Optional[str]

    @strawberry.field
    def image(
        self,
        info,
        width: Optional[int] = 1280,
        height: Optional[int] = 400,
        zoom: Optional[int] = 15,
    ) -> str:
        return generate_map_image(
            latitude=self.latitude,
            longitude=self.longitude,
            width=width,
            height=height,
            zoom=zoom,
        )


@strawberry.type
class Conference:
    id: strawberry.ID

    name: str
    code: str
    start: DateTime
    end: DateTime
    introduction: str

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
    def map(self, info) -> Optional[Map]:
        if not all((self.latitude, self.longitude)):
            return None

        return Map(
            latitude=self.latitude, longitude=self.longitude, link=self.map_link or None
        )

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
    def copy(self, info, key: str) -> Optional[str]:
        copy = GenericCopy.objects.filter(conference=self, key=key).first()

        return copy.content if copy else None


@strawberry.type
class Deadline:
    type: str
    name: str
    start: DateTime
    end: DateTime
    conference: Conference


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
