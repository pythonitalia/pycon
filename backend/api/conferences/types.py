from datetime import date, datetime, time
from typing import List, Optional

import strawberry
from django.conf import settings
from django.utils import translation
from strawberry import ID, Private

from api.cms.types import FAQ, Menu
from api.events.types import Event
from api.hotels.types import HotelRoom
from api.languages.types import Language
from api.pretix.query import get_conference_tickets, get_voucher
from api.pretix.types import TicketItem, Voucher
from api.schedule.types import Room, ScheduleItem
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
class KeynoteSpeaker:
    id: ID
    name: str
    bio: str = strawberry.field(resolver=make_localized_resolver("bio"))
    pronouns: str = strawberry.field(resolver=make_localized_resolver("pronouns"))
    twitter_handle: str
    instagram_handle: str
    website: str
    highlight_color: str
    _photo_url: Private[str]

    def __init__(
        self,
        id: ID,
        name: str,
        bio: str,
        pronouns: str,
        twitter_handle: str,
        instagram_handle: str,
        website: str,
        highlight_color: str,
        _photo_url: str,
    ):
        self.id = id
        self.name = name
        self.bio = bio
        self.pronouns = pronouns
        self.twitter_handle = twitter_handle
        self.instagram_handle = instagram_handle
        self.website = website
        self.highlight_color = highlight_color
        self._photo_url = _photo_url

    @strawberry.field
    def photo(self, info) -> str:
        return info.context.request.build_absolute_uri(self._photo_url)

    @classmethod
    def from_django_model(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
            _photo_url=instance.photo.url,
            bio=instance.bio,
            pronouns=instance.pronouns,
            highlight_color=instance.highlight_color,
            twitter_handle=instance.twitter_handle,
            instagram_handle=instance.instagram_handle,
            website=instance.website,
        )


@strawberry.type
class Keynote:
    id: ID
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    topic: Optional[Topic]
    speakers: List[KeynoteSpeaker]

    def __init__(
        self,
        id: ID,
        title: str,
        description: str,
        slug: str,
        topic: Optional[Topic],
        speakers: List[KeynoteSpeaker],
    ):
        self.id = id
        self.title = title
        self.description = description
        self.slug = slug
        self.topic = topic
        self.speakers = speakers

    @classmethod
    def from_django_model(cls, instance):
        return cls(
            id=instance.id,
            title=instance.title,
            description=instance.description,
            slug=instance.slug,
            topic=Topic.from_django_model(instance.topic) if instance.topic else None,
            speakers=[
                KeynoteSpeaker.from_django_model(speaker)
                for speaker in instance.speakers.all()
            ],
        )


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
            status=SubmissionModel.STATUS.proposed
        ).select_related("audience_level", "duration", "type", "topic")

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
    def ranking(self, info) -> Optional[RankRequest]:
        try:
            rank_requests = RankRequestModel.objects.filter(conference=self)
            if not rank_requests:
                return None

            rank_request = rank_requests[0]

            if not rank_request.is_public and not IsStaffPermission().has_permission(
                self, info
            ):
                return None

            return RankRequest(
                is_public=rank_request.is_public,
                ranked_submissions=rank_request.rank_submissions.all().order_by(
                    "absolute_rank"
                ),
            )
        except RankRequestModel.DoesNotExist:
            return None

    @strawberry.field
    def days(self, info) -> List[Day]:
        return self.days.prefetch_related("slots", "slots__items").all()


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
