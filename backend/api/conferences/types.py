from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import List, Optional

import strawberry
from django.conf import settings
from django.utils import timezone, translation
from strawberry import ID
from django.db.models import Case, When, Value, IntegerField
from api.cms.types import FAQ, Menu
from api.events.types import Event
from api.hotels.types import HotelRoom
from api.languages.types import Language
from api.pretix.query import get_conference_tickets, get_voucher
from api.pretix.types import TicketItem, Voucher
from api.schedule.types import DayRoom, ScheduleItem, ScheduleItemUser
from api.sponsors.types import SponsorsByLevel
from api.submissions.types import Submission, SubmissionType
from api.voting.types import RankRequest
from cms.models import GenericCopy
from conferences.models.deadline import DeadlineStatus
from schedule.models import ScheduleItem as ScheduleItemModel
from submissions.models import Submission as SubmissionModel
from voting.models import RankRequest as RankRequestModel

from ..helpers.i18n import make_localized_resolver
from ..helpers.maps import Map, resolve_map
from ..permissions import CanSeeSubmissions, IsStaffPermission


@strawberry.type
class AudienceLevel:
    id: strawberry.ID
    name: str


@strawberry.type
class Topic:
    id: strawberry.ID
    name: str

    @classmethod
    def from_django_model(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
        )


@strawberry.type
class Keynote:
    id: ID
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    topic: Optional[Topic]
    speakers: List[ScheduleItemUser]
    start: Optional[datetime]
    end: Optional[datetime]

    def __init__(
        self,
        id: ID,
        title: str,
        description: str,
        slug: str,
        topic: Optional[Topic],
        speakers: List[ScheduleItemUser],
        start: Optional[datetime],
        end: Optional[datetime],
    ):
        self.id = id
        self.title = title
        self.description = description
        self.slug = slug
        self.topic = topic
        self.speakers = speakers
        self.start = start
        self.end = end

    @classmethod
    def from_django_model(cls, instance):
        schedule_item = instance.schedule_item
        return cls(
            id=instance.id,
            title=instance.title,
            description=instance.description,
            slug=instance.slug,
            topic=Topic.from_django_model(instance.topic) if instance.topic else None,
            speakers=[
                ScheduleItemUser(
                    id=speaker.user_id, conference_code=instance.conference.code
                )
                for speaker in instance.speakers.all()
            ],
            start=schedule_item.start if schedule_item else None,
            end=schedule_item.end if schedule_item else None,
        )


@strawberry.enum
class ScheduleSlotType(Enum):
    DEFAULT = "default"
    FREE_TIME = "free_time"


@strawberry.type
class ScheduleSlot:
    hour: time
    duration: int
    type: ScheduleSlotType
    id: strawberry.ID

    @strawberry.field
    def end_hour(self, info) -> time:
        return (
            datetime.combine(datetime.today(), self.hour)
            + timedelta(minutes=self.duration)
        ).time()

    @strawberry.field
    def items(self, info) -> List[ScheduleItem]:
        return (
            ScheduleItemModel.objects.annotate(
                order=Case(
                    When(type="custom", then=Value(1)),
                    When(type="talk", then=Value(2)),
                    When(type="panel", then=Value(3)),
                    default=Value(4),
                    output_field=IntegerField(),
                )
            )
            .filter(slot__id=self.id)
            .select_related(
                "language",
                "audience_level",
                "submission",
                "submission__type",
                "submission__duration",
                "submission__audience_level",
                "submission__type",
            )
            .prefetch_related("additional_speakers", "rooms")
            .order_by("order")
        )


@strawberry.type
class Day:
    day: date

    @strawberry.field
    def random_events(self, limit: int = 4) -> List[ScheduleItem]:
        if limit > 10:
            raise ValueError("Limit cannot be greater than 10")

        return ScheduleItemModel.objects.filter(
            slot__day=self,
            type__in=[
                ScheduleItemModel.TYPES.talk,
                ScheduleItemModel.TYPES.training,
                ScheduleItemModel.TYPES.panel,
            ],
        ).order_by("?")[:limit]

    @strawberry.field
    def slots(self, info, room: Optional[strawberry.ID] = None) -> List[ScheduleSlot]:
        if room:
            return list(self.slots.filter(items__rooms__id=room))
        return list(self.slots.all())

    @strawberry.field
    def running_events(self, info) -> List[ScheduleItem]:
        current_slot = self.slots.filter(
            hour__lte=timezone.now().astimezone(self.conference.timezone)
        ).last()

        if not current_slot:
            return []

        return [item for item in current_slot.items.all()]

    @strawberry.field
    def rooms(self) -> List[DayRoom]:
        data = self.added_rooms.values(
            "room__id", "streaming_url", "slido_url", "room__type", "room__name"
        )
        return [
            DayRoom(
                id=room["room__id"],
                name=room["room__name"],
                type=room["room__type"],
                streaming_url=room["streaming_url"],
                slido_url=room["slido_url"],
            )
            for room in data
        ]

    @classmethod
    def from_db(cls, instance):
        obj = cls(day=instance.day)
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
    def tickets(
        self, info, language: str, show_unavailable_tickets: bool = False
    ) -> List[TicketItem]:
        return get_conference_tickets(
            self, language=language, show_unavailable_tickets=show_unavailable_tickets
        )

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
        return self.submissions.filter(
            status__in=(
                SubmissionModel.STATUS.proposed,
                SubmissionModel.STATUS.accepted,
            )
        ).select_related("audience_level", "duration", "type", "topic")

    @strawberry.field
    def events(self, info) -> List[Event]:
        return self.events.all()

    @strawberry.field
    def faqs(self, info) -> List[FAQ]:
        return self.faqs.all()

    @strawberry.field
    def sponsors_by_level(self, info) -> List[SponsorsByLevel]:
        levels = self.sponsor_levels.all().order_by("order")

        return [SponsorsByLevel.from_model(level) for level in levels]

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
    def keynotes(self, info) -> List[Keynote]:
        return [Keynote.from_django_model(keynote) for keynote in self.keynotes.all()]

    @strawberry.field
    def keynote(self, info, slug: str) -> Optional[Keynote]:
        keynote = self.keynotes.by_slug(slug).first()
        return Keynote.from_django_model(keynote) if keynote else None

    @strawberry.field
    def talks(self, info) -> List[ScheduleItem]:
        return self.schedule_items.filter(type=ScheduleItemModel.TYPES.submission).all()

    @strawberry.field
    def talk(self, info, slug: str) -> Optional[ScheduleItem]:
        return self.schedule_items.filter(slug=slug).first()

    @strawberry.field
    def ranking(self, info, topic: strawberry.ID) -> Optional[RankRequest]:
        rank_request = RankRequestModel.objects.filter(conference=self).first()
        if not rank_request:
            return None

        if not rank_request.is_public and not IsStaffPermission().has_permission(
            self, info
        ):
            return None

        submissions = rank_request.rank_submissions.filter(
            submission__topic__id=topic
        ).order_by("rank")
        return RankRequest(
            is_public=rank_request.is_public,
            ranked_submissions=submissions,
            stats=rank_request.stats.all(),
        )

    @strawberry.field
    def days(self, info) -> List[Day]:
        return self.days.order_by("day").prefetch_related("slots", "slots__items").all()

    @strawberry.field
    def is_running(self, info) -> bool:
        now = timezone.now()
        return self.start <= now <= self.end


DeadlineStatusType = strawberry.enum(DeadlineStatus)


@strawberry.type
class Deadline:
    id: strawberry.ID
    type: str
    name: str = strawberry.field(resolver=make_localized_resolver("name"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    start: datetime
    end: datetime
    conference: Conference
    status: DeadlineStatusType


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
