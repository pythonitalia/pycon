from api.context import Info
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Prefetch
from participants.models import Participant as ParticipantModel
from datetime import datetime
from api.participants.types import Participant
from api.schedule.types.day import Day

import strawberry
from django.conf import settings
from django.utils import timezone, translation
from strawberry import ID
from api.cms.types import FAQ, Menu
from api.events.types import Event
from api.languages.types import Language
from api.pretix.query import get_conference_tickets, get_voucher
from api.pretix.types import TicketItem, Voucher
from api.schedule.types import Room, ScheduleItem, ScheduleItemUser
from api.sponsors.types import (
    SponsorBenefit,
    SponsorLevel,
    SponsorLevelBenefit,
    SponsorSpecialOption,
    SponsorsByLevel,
)
from api.submissions.types import Submission, SubmissionTag, SubmissionType
from api.voting.types import RankRequest
from cms.models import GenericCopy
from conferences.models.deadline import DeadlineStatus
from schedule.models import ScheduleItem as ScheduleItemModel
from submissions.models import Submission as SubmissionModel
from voting.models import RankRequest as RankRequestModel
from sponsors.models import SponsorLevel as SponsorLevelModel

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


DeadlineStatusType = strawberry.enum(DeadlineStatus)


@strawberry.type
class Deadline:
    id: strawberry.ID
    type: str
    name: str = strawberry.field(resolver=make_localized_resolver("name"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    start: datetime
    end: datetime
    status: DeadlineStatusType


@strawberry.type
class Keynote:
    id: ID
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    topic: Topic | None
    speakers: list[ScheduleItemUser]
    start: datetime | None
    end: datetime | None
    rooms: list[Room]
    youtube_video_id: str | None

    def __init__(
        self,
        id: ID,
        title: str,
        description: str,
        slug: str,
        topic: Topic | None,
        speakers: list[ScheduleItemUser],
        start: datetime | None,
        end: datetime | None,
        rooms: list[Room],
        youtube_video_id: str | None,
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
            participants_data = {
                participant.user_id: participant
                for participant in ParticipantModel.objects.filter(
                    user_id__in=instance.speakers.values_list("user_id"),
                    conference_id=instance.conference_id,
                ).all()
            }

        schedule_item = instance.schedule_items.all().first()

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
    map: Map | None = strawberry.field(resolver=resolve_map)

    pretix_event_url: str

    @strawberry.field
    def voucher(self, info: Info, code: str) -> Voucher | None:
        return get_voucher(self, code)

    @strawberry.field
    def timezone(self, info: Info) -> str:
        return str(self.timezone)

    @strawberry.field
    def tickets(
        self, info: Info, language: str, show_unavailable_tickets: bool = False
    ) -> list[TicketItem]:
        return get_conference_tickets(
            self, language=language, show_unavailable_tickets=show_unavailable_tickets
        )

    @strawberry.field
    def deadlines(self, info: Info) -> list[Deadline]:
        return self.deadlines.order_by("start").all()

    @strawberry.field(name="isCFPOpen")
    def is_cfp_open(self, info: Info) -> bool:
        return self.is_cfp_open

    @strawberry.field
    def is_voting_open(self, info: Info) -> bool:
        return self.is_voting_open

    @strawberry.field
    def is_voting_closed(self, info: Info) -> bool:
        return self.is_voting_closed

    @strawberry.field
    def deadline(self, info: Info, type: str) -> Deadline | None:
        return self.deadlines.filter(type=type).first()

    @strawberry.field
    def audience_levels(self, info: Info) -> list[AudienceLevel]:
        return self.audience_levels.all()

    @strawberry.field
    def topics(self, info: Info) -> list[Topic]:
        return self.topics.all()

    @strawberry.field
    def languages(self, info: Info) -> list[Language]:
        return self.languages.all()

    @strawberry.field
    def durations(self, info: Info) -> list["Duration"]:
        return self.durations.all()

    @strawberry.field
    def submission_types(self, info: Info) -> list[SubmissionType]:
        return self.submission_types.all()

    @strawberry.field
    def proposal_tags(self, info: Info) -> list[SubmissionTag]:
        return self.proposal_tags.all()

    @strawberry.field(permission_classes=[CanSeeSubmissions])
    def submissions(self, info: Info) -> list[Submission] | None:
        return self.submissions.filter(
            status__in=(
                SubmissionModel.STATUS.proposed,
                SubmissionModel.STATUS.accepted,
            )
        ).select_related("audience_level", "duration", "type", "topic")

    @strawberry.field
    def events(self, info: Info) -> list[Event]:
        return self.events.all()

    @strawberry.field
    def faqs(self, info: Info) -> list[FAQ]:
        return self.faqs.all()

    @strawberry.field
    def sponsors_by_level(self, info: Info) -> list[SponsorsByLevel]:
        levels = self.sponsor_levels.all().order_by("order")

        return [SponsorsByLevel.from_model(level) for level in levels]

    @strawberry.field
    def copy(self, info: Info, key: str, language: str | None = None) -> str | None:
        copy = GenericCopy.objects.filter(conference=self, key=key).first()

        language = language or translation.get_language() or settings.LANGUAGE_CODE

        return copy.content.localize(language) if copy else None

    @strawberry.field
    def menu(self, info: Info, identifier: str) -> Menu | None:
        return (
            self.menus.filter(identifier=identifier).prefetch_related("links").first()
        )

    @strawberry.field
    def keynotes(self, info: Info) -> list[Keynote]:
        return [
            Keynote.from_django_model(keynote, info) for keynote in self.keynotes.all()
        ]

    @strawberry.field
    def keynote(self, info: Info, slug: str) -> Keynote | None:
        keynote = self.keynotes.by_slug(slug).first()
        return Keynote.from_django_model(keynote, info) if keynote else None

    @strawberry.field
    def talks(self, info: Info) -> list[ScheduleItem]:
        return self.schedule_items.filter(type=ScheduleItemModel.TYPES.submission).all()

    @strawberry.field
    def talk(self, info: Info, slug: str) -> ScheduleItem | None:
        return self.schedule_items.filter(slug=slug).first()

    @strawberry.field
    def ranking(self, info: Info, topic: strawberry.ID) -> RankRequest | None:
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
    def days(self, info: Info) -> list[Day]:
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
                                When(type="break", then=Value(1)),
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
    def current_day(self, info: Info) -> Day | None:
        start = timezone.now().replace(hour=0, minute=0, second=0)
        end = start.replace(hour=23, minute=59, second=59)
        return self.days.filter(day__gte=start, day__lte=end).first()

    @strawberry.field
    def is_running(self, info: Info) -> bool:
        now = timezone.now()
        return self.start <= now <= self.end

    @strawberry.field
    def sponsor_benefits(self) -> list[SponsorBenefit]:
        benefits = self.sponsor_benefits.order_by("order").all()

        return [
            SponsorBenefit(
                name=benefit.name,
                category=benefit.category,
                description=benefit.description,
            )
            for benefit in benefits
        ]

    @strawberry.field
    def sponsor_levels(self) -> list[SponsorLevel]:
        levels = (
            SponsorLevelModel.objects.filter(conference=self)
            .prefetch_related(
                "sponsorlevelbenefit_set",
                "sponsorlevelbenefit_set__benefit",
            )
            .order_by("order")
        )

        return [
            SponsorLevel(
                name=level.name,
                price=level.price,
                slots=level.slots,
                benefits=[
                    SponsorLevelBenefit(
                        name=level_benefit.benefit.name,
                        category=level_benefit.benefit.category,
                        value=level_benefit.value,
                        description=level_benefit.benefit.description,
                    )
                    for level_benefit in level.sponsorlevelbenefit_set.all()
                ],
            )
            for level in levels
        ]

    @strawberry.field
    def sponsor_special_options(self) -> list[SponsorSpecialOption]:
        options = self.sponsor_special_options.order_by("order").all()

        return [
            SponsorSpecialOption(
                name=option.name,
                description=option.description,
                price=option.price,
            )
            for option in options
        ]


@strawberry.type
class Duration:
    id: strawberry.ID
    conference: Conference
    name: str
    duration: int
    notes: str

    @strawberry.field
    def allowed_submission_types(self, info: Info) -> list[SubmissionType]:
        return self.allowed_submission_types.all()
