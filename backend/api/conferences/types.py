from itertools import groupby
from typing import List, Optional
from datetime import time, date, datetime
import strawberry
from api.cms.types import FAQ, Menu
from api.events.types import Event
from api.hotels.types import HotelRoom
from api.languages.types import Language
from api.pretix.query import get_conference_tickets, get_voucher
from api.pretix.types import TicketItem, Voucher
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
class ScheduleSlot:
    hour: time
    duration: int
    id: strawberry.ID

    @strawberry.field
    def items(self, info) -> List[ScheduleItem]:
        return (
            ScheduleItemModel.objects.filter(slot__id=self.id)
            .select_related(
                "language",
                "audience_level",
                "submission",
                "submission__speaker",
                "submission__type",
                "submission__duration",
                "submission__audience_level",
                "submission__type",
            )
            .prefetch_related("additional_speakers", "rooms")
        )


@strawberry.type
class Day:
    day: date

    @strawberry.field
    def slots(self, info, room: Optional[strawberry.ID] = None) -> List[ScheduleSlot]:
        if room:
            return list(self.slots.filter(items__rooms__id=room))
        return list(self.slots.all())

    @classmethod
    def from_db(cls, instance):
        obj = cls(instance.day)
        obj.slots = instance.slots
        return obj


@strawberry.type
class Conference:
    id: strawberry.ID

    name: str = strawberry.field(resolver=make_localized_resolver("name"))
    introduction: str = strawberry.field(
        resolver=make_localized_resolver("introduction")
    )
    code: str
    start: datetime
    end: datetime
    map: Optional[Map] = strawberry.field(resolver=resolve_map)

    pretix_event_url: str

    @strawberry.field
    def voucher(self, info, code: str) -> Optional[Voucher]:
        return get_voucher(self, code)

    @strawberry.field
    def timezone(self, info) -> str:
        return str(self.timezone)

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
    def is_voting_closed(self, info) -> bool:
        return self.is_voting_closed

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

        sponsors = (
            Sponsor.objects.filter(level__conference__code=self.code)
            .order_by("level", "order")
            .select_related("level")
        )

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
    def talks(self, info) -> List[ScheduleItem]:
        return self.schedule_items.filter(type=ScheduleItemModel.TYPES.submission).all()

    @strawberry.field
    def talk(self, info, slug: str) -> Optional[ScheduleItem]:
        return self.schedule_items.filter(slug=slug).first()

    @strawberry.field
    def ranking(self, info) -> List[RankSubmission]:
        try:
            return (
                RankRequestModel.objects.get(conference=self)
                .rank_submissions.all()
                .order_by("absolute_rank")
            )
        except RankRequestModel.DoesNotExist:
            return []

    @strawberry.field
    def days(self, info) -> List[Day]:
        return self.days.prefetch_related("slots", "slots__items").all()


@strawberry.type
class Deadline:
    type: str
    name: str = strawberry.field(resolver=make_localized_resolver("name"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    start: datetime
    end: datetime
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
