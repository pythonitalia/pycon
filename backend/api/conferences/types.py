from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import List, Optional

import strawberry
from django.conf import settings
from django.utils import timezone, translation
from strawberry import ID

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
from schedule.models import Day as DayModel
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
    def from_django_model(cls, instance, schedule_item):
        return cls(
            id=instance.id,
            title=instance.title,
            description=instance.description,
            slug=instance.slug,
            topic=Topic.from_django_model(instance.topic)
            if instance.topic_id
            else None,
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
    async def items(self, info) -> List[ScheduleItem]:
        return [
            item
            async for item in ScheduleItemModel.objects.filter(slot__id=self.id)
            .select_related(
                "language",
                "audience_level",
                "submission",
                "submission__type",
                "submission__duration",
                "submission__audience_level",
                "submission__type",
            )
            .prefetch_related(
                "additional_speakers", "rooms", "attendees", "conference", "keynote"
            )
            .all()
        ]


@strawberry.type
class Day:
    day: date

    @strawberry.field
    async def slots(
        self, info, room: Optional[strawberry.ID] = None
    ) -> List[ScheduleSlot]:
        if room:
            return [slot async for slot in self.slots.filter(items__rooms__id=room)]
        return [slot async for slot in self.slots.all()]

    @strawberry.field
    async def running_events(self, info) -> List[ScheduleItem]:
        current_slot = await self.slots.filter(
            hour__lte=timezone.now().astimezone(self.conference.timezone)
        ).alast()

        if not current_slot:
            return []

        return [item async for item in current_slot.items.all()]

    @strawberry.field
    async def rooms(self) -> List[DayRoom]:
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
            async for room in data
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
    async def hotel_rooms(self, info) -> List[HotelRoom]:
        return [hotel_room async for hotel_room in self.hotel_rooms.all()]

    @strawberry.field
    async def deadlines(self, info) -> List["Deadline"]:
        return [deadline async for deadline in self.deadlines.order_by("start").all()]

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
    async def deadline(self, info, type: str) -> Optional["Deadline"]:
        return await self.deadlines.filter(type=type).afirst()

    @strawberry.field
    async def audience_levels(self, info) -> List[AudienceLevel]:
        return [audience_level async for audience_level in self.audience_levels.all()]

    @strawberry.field
    async def topics(self, info) -> List[Topic]:
        return [topic async for topic in self.topics.all()]

    @strawberry.field
    async def languages(self, info) -> List[Language]:
        return [language async for language in self.languages.all()]

    @strawberry.field
    async def durations(self, info) -> List["Duration"]:
        return [duration async for duration in self.durations.all()]

    @strawberry.field
    async def submission_types(self, info) -> List[SubmissionType]:
        return [
            submission_type async for submission_type in self.submission_types.all()
        ]

    @strawberry.field(permission_classes=[CanSeeSubmissions])
    async def submissions(self, info) -> Optional[List[Submission]]:
        return [
            submission
            for submission in self.submissions.filter(
                status__in=(
                    SubmissionModel.STATUS.proposed,
                    SubmissionModel.STATUS.accepted,
                )
            ).select_related("audience_level", "duration", "type", "topic")
        ]

    @strawberry.field
    async def events(self, info) -> List[Event]:
        return [event async for event in self.events.all()]

    @strawberry.field
    async def faqs(self, info) -> List[FAQ]:
        return [faq async for faq in self.faqs.all()]

    @strawberry.field
    async def sponsors_by_level(self, info) -> List[SponsorsByLevel]:
        levels = self.sponsor_levels.all().order_by("order")

        return [SponsorsByLevel.from_model(level) async for level in levels]

    @strawberry.field
    async def copy(
        self, info, key: str, language: Optional[str] = None
    ) -> Optional[str]:
        copy = await GenericCopy.objects.filter(conference=self, key=key).afirst()

        language = language or translation.get_language() or settings.LANGUAGE_CODE

        return copy.content.localize(language) if copy else None

    @strawberry.field
    async def menu(self, info, identifier: str) -> Optional[Menu]:
        return (
            self.menus.filter(identifier=identifier).prefetch_related("links").afirst()
        )

    @strawberry.field
    async def keynotes(self, info) -> List[Keynote]:
        return [
            Keynote.from_django_model(keynote) async for keynote in self.keynotes.all()
        ]

    @strawberry.field
    async def keynote(self, info, slug: str) -> Optional[Keynote]:
        keynote = await self.keynotes.by_slug(slug).afirst()
        return Keynote.from_django_model(keynote) if keynote else None

    @strawberry.field
    async def talks(self, info) -> List[ScheduleItem]:
        return [
            schedule_item
            async for schedule_item in self.schedule_items.filter(
                type=ScheduleItemModel.TYPES.submission
            ).all()
        ]

    @strawberry.field
    async def talk(self, info, slug: str) -> Optional[ScheduleItem]:
        return await self.schedule_items.filter(slug=slug).afirst()

    @strawberry.field
    async def ranking(self, info, topic: strawberry.ID) -> Optional[RankRequest]:
        rank_request = (
            await RankRequestModel.objects.select_related()
            .filter(conference=self)
            .afirst()
        )
        if not rank_request:
            return None

        if not rank_request.is_public and not IsStaffPermission().has_permission(
            self, info
        ):
            return None

        submissions = (
            await rank_request.rank_submissions.filter(submission__topic__id=topic)
            .order_by("rank")
            .all()
        )
        return RankRequest(
            is_public=rank_request.is_public,
            ranked_submissions=submissions,
            stats=rank_request.stats.all(),
        )

    @strawberry.field
    async def days(self) -> List[Day]:
        return [
            day
            async for day in DayModel.objects.filter(conference_id=self.id)
            .order_by("day")
            .prefetch_related("slots", "slots__items", "conference")
        ]

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
    async def allowed_submission_types(self, info) -> List[SubmissionType]:
        return [
            submission_type
            async for submission_type in self.allowed_submission_types.all()
        ]
