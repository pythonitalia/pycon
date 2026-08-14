from datetime import datetime

import strawberry
import strawberry_django
from django.conf import settings
from django.db.models import prefetch_related_objects
from django.utils import timezone, translation

from api.cms.types import FAQ, Menu
from api.context import Info
from api.events.types import Event
from api.generic_forms.types import Form as GenericForm
from api.generic_forms.types import FormPurpose
from api.languages.types import Language
from api.pretix.query import get_conference_tickets, get_voucher
from api.pretix.types import TicketItem, Voucher
from api.schedule.types import Room, ScheduleItem, ScheduleItemUser
from api.schedule.types.day import Day
from api.sponsors.types import (
    SponsorBenefit,
    SponsorLevel,
    SponsorLevelBenefit,
    SponsorsByLevel,
    SponsorSpecialOption,
)
from api.submissions.types import Submission, SubmissionTag, SubmissionType
from api.voting.types import RankRequest
from cms import models as cms_models
from conferences import models as conference_models
from conferences.models import deadline as deadline_models
from participants import models as participant_models
from schedule import models as schedule_models
from sponsors import models as sponsor_models
from submissions import models as submission_models
from voting import models as voting_models

from ..helpers.i18n import make_localized_resolver
from ..helpers.maps import Map, resolve_map
from ..permissions import CanSeeSubmissions, IsStaffPermission


@strawberry_django.type(conference_models.AudienceLevel)
class AudienceLevel:
    id: strawberry.auto
    name: strawberry.auto


@strawberry_django.type(conference_models.Topic)
class Topic:
    id: strawberry.auto
    name: strawberry.auto

    @classmethod
    def from_django_model(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
        )


DeadlineStatus = strawberry.enum(deadline_models.DeadlineStatus)


@strawberry_django.type(conference_models.Deadline)
class Deadline:
    id: strawberry.auto
    type: str = strawberry_django.field(only=["type"])
    name: str = strawberry_django.field(
        resolver=make_localized_resolver("name"), only=["name"]
    )
    description: str = strawberry_django.field(
        resolver=make_localized_resolver("description"), only=["description"]
    )
    start: datetime = strawberry_django.field(only=["start"])
    end: datetime = strawberry_django.field(only=["end"])
    status: DeadlineStatus = strawberry_django.field(only=["start", "end"])


def _keynote_schedule_item(keynote):
    return min(keynote.schedule_items.all(), key=lambda item: item.pk, default=None)


@strawberry_django.type(conference_models.Keynote)
class Keynote:
    id: strawberry.auto
    title: str = strawberry_django.field(
        resolver=make_localized_resolver("title"), only=["title"]
    )
    description: str = strawberry_django.field(
        resolver=make_localized_resolver("description"), only=["description"]
    )
    slug: str = strawberry_django.field(
        resolver=make_localized_resolver("slug"), only=["slug"]
    )
    topic: Topic | None

    # Keep model instances here: values()/values_list() bypass Django's prefetch
    # cache. A narrower custom Prefetch is only worthwhile if profiling shows it.
    @strawberry_django.field(prefetch_related=["speakers__user"])
    def speakers(self, info: Info) -> list[ScheduleItemUser]:
        keynote_speakers = [
            speaker for speaker in self.speakers.all() if speaker.user_id
        ]
        participants_data = info.context._participants_data
        if not participants_data:
            participants_data = {
                participant.user_id: participant
                for participant in participant_models.Participant.objects.filter(
                    user_id__in=[speaker.user_id for speaker in keynote_speakers],
                    conference_id=self.conference_id,
                ).all()
            }

        return [
            ScheduleItemUser(
                id=speaker.user_id,
                fullname=speaker.user.full_name,
                full_name=speaker.user.full_name,
                participant=participants_data[speaker.user_id],
            )
            for speaker in keynote_speakers
        ]

    @strawberry_django.field(prefetch_related=["schedule_items"])
    def start(self) -> datetime | None:
        schedule_item = _keynote_schedule_item(self)
        return schedule_item.start if schedule_item else None

    @strawberry_django.field(prefetch_related=["schedule_items"])
    def end(self) -> datetime | None:
        schedule_item = _keynote_schedule_item(self)
        return schedule_item.end if schedule_item else None

    @strawberry_django.field(prefetch_related=["schedule_items__rooms"])
    def rooms(self) -> list[Room]:
        schedule_item = _keynote_schedule_item(self)
        return schedule_item.rooms.all() if schedule_item else []

    @strawberry_django.field(prefetch_related=["schedule_items"])
    def youtube_video_id(self) -> str | None:
        schedule_item = _keynote_schedule_item(self)
        return schedule_item.youtube_video_id if schedule_item else None


@strawberry_django.type(conference_models.Conference)
class Conference:
    id: strawberry.auto

    name: str = strawberry_django.field(
        resolver=make_localized_resolver("name"), only=["name"]
    )
    introduction: str = strawberry_django.field(
        resolver=make_localized_resolver("introduction"), only=["introduction"]
    )
    code: strawberry.auto
    hostname: strawberry.auto
    start: datetime
    end: datetime
    map: Map | None = strawberry.field(resolver=resolve_map)

    pretix_event_url: strawberry.auto

    @strawberry_django.field(
        only=["pretix_organizer_id", "pretix_event_id"],
    )
    def voucher(self, info: Info, code: str) -> Voucher | None:
        return get_voucher(self, code)

    @strawberry_django.field(only=["timezone"])
    def timezone(self, info: Info) -> str:
        return str(self.timezone)

    @strawberry.field
    def tickets(
        self, info: Info, language: str, show_unavailable_tickets: bool = False
    ) -> list[TicketItem]:
        return get_conference_tickets(
            self, language=language, show_unavailable_tickets=show_unavailable_tickets
        )

    @strawberry_django.field
    def deadlines(self) -> list[Deadline]:
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

    # Strawberry resolves each aliased field separately. Django's prefetch cache
    # makes this a no-op after the first alias, avoiding one query per deadline.
    @strawberry_django.field
    def deadline(self, type: str) -> Deadline | None:
        prefetch_related_objects([self], "deadlines")
        return next(
            (deadline for deadline in self.deadlines.all() if deadline.type == type),
            None,
        )

    @strawberry.field
    def form(self, info: Info, purpose: FormPurpose) -> GenericForm | None:
        return self.forms.filter(purpose=purpose).first()

    @strawberry.field
    def audience_levels(self, info: Info) -> list[AudienceLevel]:
        return self.audience_levels.all()

    @strawberry.field
    def topics(self, info: Info) -> list[Topic]:
        return self.topics.all()

    @strawberry.field
    def languages(self, info: Info) -> list[Language]:
        return self.languages.all()

    durations: list["Duration"]

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
                submission_models.Submission.STATUS.proposed,
                submission_models.Submission.STATUS.accepted,
            )
        ).select_related("audience_level", "duration", "type", "topic")

    @strawberry.field
    def events(self, info: Info) -> list[Event]:
        return self.events.all()

    @strawberry.field
    def faqs(self, info: Info) -> list[FAQ]:
        return self.faqs.all()

    @strawberry_django.field
    def sponsors_by_level(self) -> list[SponsorsByLevel]:
        return self.sponsor_levels.all()

    @strawberry.field
    def copy(self, info: Info, key: str, language: str | None = None) -> str | None:
        copy = cms_models.GenericCopy.objects.filter(conference=self, key=key).first()

        language = language or translation.get_language() or settings.LANGUAGE_CODE

        return copy.content.localize(language) if copy else None

    @strawberry_django.field
    def menu(self, identifier: str) -> Menu | None:
        return self.menus.filter(identifier=identifier)

    @strawberry_django.field
    def keynotes(self, info: Info) -> list[Keynote]:
        return self.keynotes.all()

    @strawberry_django.field
    def keynote(self, info: Info, slug: str) -> Keynote | None:
        return self.keynotes.by_slug(slug)

    @strawberry_django.field
    def talks(self) -> list[ScheduleItem]:
        return self.schedule_items.filter(
            type=schedule_models.ScheduleItem.TYPES.submission
        )

    @strawberry_django.field
    def talk(self, info: Info, slug: str) -> ScheduleItem | None:
        return self.schedule_items.filter(slug=slug)

    @strawberry.field
    def ranking(self, info: Info, topic: strawberry.ID) -> RankRequest | None:
        rank_request = voting_models.RankRequest.objects.filter(conference=self).first()
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

    @strawberry_django.field
    def days(self, info: Info) -> list[Day]:
        return self.days.all()

    @strawberry_django.field
    def current_day(self) -> Day | None:
        start = timezone.now().replace(hour=0, minute=0, second=0)
        end = start.replace(hour=23, minute=59, second=59)
        return self.days.filter(day__gte=start, day__lte=end)

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
            sponsor_models.SponsorLevel.objects.filter(conference=self)
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


@strawberry_django.type(conference_models.Duration)
class Duration:
    id: strawberry.auto
    conference: Conference
    name: strawberry.auto
    duration: strawberry.auto
    notes: strawberry.auto
    allowed_submission_types: list[SubmissionType]
