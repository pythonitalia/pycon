from django.db.models import Case, When, Value, IntegerField
from django.db.models import Prefetch
from participants.models import Participant as ParticipantModel
from datetime import datetime
from typing import List, Optional
from api.participants.types import Participant
from api.schedule.types.day import Day

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
from api.schedule.types import Room, ScheduleItem, ScheduleItemUser
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
    rooms: List[Room]
    youtube_video_id: Optional[str]

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
        rooms: List[Room],
        youtube_video_id: Optional[str],
    ):
        self.id = id
        self.title = title
        self.description = description
        self.slug = slug
        self.topic = topic
        self.speakers = speakers
        self.start = start
        self.end = end
        self.rooms = rooms
        self.youtube_video_id = youtube_video_id

    @classmethod
    def from_django_model(cls, instance, info):
        participants_data = info.context._participants_data
        if not participants_data:
            participants_data = ParticipantModel.objects.get(
                user_id__in=instance.speakers.values_list("user_id"),
                conference_id=instance.conference_id,
            )

        schedule_item = instance.schedule_items.all()[0]

        return cls(
            id=instance.id,
            title=instance.title,
            description=instance.description,
            slug=instance.slug,
            topic=Topic.from_django_model(instance.topic) if instance.topic else None,
            speakers=[
                ScheduleItemUser(
                    id=speaker.user_id,
                    fullname=speaker.user.full_name,
                    full_name=speaker.user.full_name,
                    participant=Participant.from_model(
                        participants_data[speaker.user_id]
                    ),
                )
                for speaker in instance.speakers.all()
            ],
            start=schedule_item.start if schedule_item else None,
            end=schedule_item.end if schedule_item else None,
            rooms=schedule_item.rooms.all() if schedule_item else [],
            youtube_video_id=schedule_item.youtube_video_id if schedule_item else None,
        )


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
    visa_application_form_link: str

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
        return [
            Keynote.from_django_model(keynote, info) for keynote in self.keynotes.all()
        ]

    @strawberry.field
    def keynote(self, info, slug: str) -> Optional[Keynote]:
        keynote = self.keynotes.by_slug(slug).first()
        return Keynote.from_django_model(keynote, info) if keynote else None

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
        days = list(
            self.days.order_by("day")
            .prefetch_related(
                "slots",
                "slots__day",
                "slots__day__added_rooms",
                "slots__day__added_rooms__room",
                Prefetch(
                    "slots__items",
                    queryset=(
                        ScheduleItemModel.objects.for_conference(self.id)
                        .annotate(
                            order=Case(
                                When(type="custom", then=Value(1)),
                                When(type="talk", then=Value(2)),
                                When(type="panel", then=Value(3)),
                                default=Value(4),
                                output_field=IntegerField(),
                            )
                        )
                        .order_by("order")
                        .prefetch_related(
                            "audience_level",
                            "language",
                            "rooms",
                            "additional_speakers",
                            "additional_speakers__user",
                            "language",
                            "submission",
                            "submission__type",
                            "submission__tags",
                            "submission__duration",
                            "submission__audience_level",
                            "submission__speaker",
                            "submission__languages",
                            "submission__schedule_items",
                            "keynote",
                            "keynote__schedule_items",
                            "keynote__schedule_items__rooms",
                            "keynote__schedule_items__slot",
                            "keynote__schedule_items__slot__day",
                            "keynote__speakers",
                            "keynote__speakers__user",
                        )
                    ),
                ),
            )
            .all()
        )
        all_speakers = [
            speaker.id
            for day in days
            for slot in day.slots.all()
            for item in slot.items.all()
            for speaker in item.speakers
        ]
        info.context._participants_data = {
            participant.user_id: participant
            for participant in ParticipantModel.objects.for_conference(self.id)
            .filter(user_id__in=all_speakers)
            .prefetch_related("user")
            .all()
        }

        return days

    @strawberry.field
    def current_day(self, info) -> Optional[Day]:
        start = timezone.now().replace(hour=0, minute=0, second=0)
        end = start.replace(hour=23, minute=59, second=59)
        return self.days.filter(day__gte=start, day__lte=end).first()

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
