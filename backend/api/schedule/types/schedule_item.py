from datetime import datetime
from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django
from django.db import models as django_models
from django.db.models.functions import Coalesce

from api.context import Info
from api.languages.types import Language
from api.permissions import IsStaffPermission
from api.schedule.types.room import Room
from api.schedule.types.schedule_item_user import ScheduleItemUser
from api.submissions.types import Submission
from participants import models as participant_models
from schedule import models

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import AudienceLevel, Conference, Keynote


ATTENDEES_COUNT_ANNOTATION = "graphql_attendees_count"
CAPACITY_ANNOTATION = "graphql_attendees_total_capacity"
USER_HAS_SPOT_ANNOTATION = "graphql_user_has_spot"


def attendees_count_annotation(_info: Info):
    return django_models.Count("attendees", distinct=True)


def capacity_annotation(_info: Info):
    room_capacity = (
        models.Room.objects.filter(talks=django_models.OuterRef("pk"))
        .order_by("pk")
        .values("attendees_total_capacity")[:1]
    )
    return Coalesce(
        "attendees_total_capacity",
        django_models.Subquery(room_capacity),
        output_field=django_models.PositiveIntegerField(),
    )


def user_has_spot_annotation(info: Info):
    user_id = info.context.request.user.id
    if not user_id:
        return django_models.Value(False, output_field=django_models.BooleanField())

    return django_models.Exists(
        models.ScheduleItemAttendee.objects.filter(
            schedule_item_id=django_models.OuterRef("pk"),
            user_id=user_id,
        )
    )


def _capacity(schedule_item) -> int | None:
    try:
        return schedule_item.graphql_attendees_total_capacity
    except AttributeError:
        return schedule_item.actual_attendees_total_capacity


def _attendees_count(schedule_item) -> int:
    try:
        return schedule_item.graphql_attendees_count
    except AttributeError:
        return schedule_item.attendees.count()


@strawberry_django.type(models.ScheduleItem)
class ScheduleItem:
    id: strawberry.auto
    conference: Annotated["Conference", strawberry.lazy("api.conferences.types")]
    title: strawberry.auto
    start: datetime
    end: datetime
    status: strawberry.auto
    submission: Submission | None
    slug: str
    description: strawberry.auto
    type: str
    duration: strawberry.auto
    highlight_color: str | None
    language: Language
    audience_level: (
        Annotated["AudienceLevel", strawberry.lazy("api.conferences.types")] | None
    )
    youtube_video_id: str | None
    link_to: strawberry.auto

    abstract: str
    elevator_pitch: str
    talk_manager: ScheduleItemUser | None = strawberry.field(
        permission_classes=[IsStaffPermission]
    )
    livestreaming_room: Room | None

    @classmethod
    def get_queryset(cls, queryset, info: Info):
        return queryset.annotate(
            graphql_order=django_models.Case(
                django_models.When(type="custom", then=django_models.Value(1)),
                django_models.When(type="break", then=django_models.Value(1)),
                django_models.When(type="talk", then=django_models.Value(2)),
                django_models.When(type="panel", then=django_models.Value(3)),
                default=django_models.Value(4),
                output_field=django_models.IntegerField(),
            )
        ).order_by("graphql_order")

    @strawberry_django.field(
        annotate={CAPACITY_ANNOTATION: capacity_annotation},
    )
    def has_limited_capacity(self) -> bool:
        return _capacity(self) is not None

    @strawberry_django.field(
        annotate={
            ATTENDEES_COUNT_ANNOTATION: attendees_count_annotation,
            CAPACITY_ANNOTATION: capacity_annotation,
        },
    )
    def has_spaces_left(self) -> bool:
        capacity = _capacity(self)
        if capacity is None:
            return True

        return capacity - _attendees_count(self) > 0

    @strawberry_django.field(
        annotate={
            ATTENDEES_COUNT_ANNOTATION: attendees_count_annotation,
            CAPACITY_ANNOTATION: capacity_annotation,
        },
    )
    def spaces_left(self) -> int:
        capacity = _capacity(self)
        if capacity is None:
            return 0

        return capacity - _attendees_count(self)

    @strawberry_django.field(
        annotate={USER_HAS_SPOT_ANNOTATION: user_has_spot_annotation},
    )
    def user_has_spot(self, info: Info) -> bool:
        try:
            return self.graphql_user_has_spot
        except AttributeError:
            user_id = info.context.request.user.id
            return self.attendees.filter(user_id=user_id).exists()

    @strawberry.field
    def user_is_talk_manager(self, info: Info) -> bool:
        if not (user_id := info.context.request.user.id):
            return False

        return self.talk_manager_id == user_id

    @strawberry_django.field(
        only=["conference_id"],
        select_related=["submission__speaker"],
        prefetch_related=[
            "keynote__speakers__user",
            "additional_speakers__user",
        ],
    )
    def speakers(self, info: Info) -> list[ScheduleItemUser]:
        speakers = []

        participants_data = info.context._participants_data
        if participants_data is None:
            schedule_items = models.ScheduleItem.objects.filter(
                conference_id=self.conference_id
            )
            submission_speakers = schedule_items.values("submission__speaker_id")
            keynote_speakers = schedule_items.values("keynote__speakers__user_id")
            additional_speakers = schedule_items.values("additional_speakers__user_id")
            participants_data = {
                participant.user_id: participant
                for participant in participant_models.Participant.objects.filter(
                    conference_id=self.conference_id
                )
                .filter(
                    django_models.Q(user_id__in=submission_speakers)
                    | django_models.Q(user_id__in=keynote_speakers)
                    | django_models.Q(user_id__in=additional_speakers)
                )
                .select_related("user")
            }
            info.context._participants_data = participants_data

        schedule_item_speakers = []
        if self.submission_id:
            schedule_item_speakers.append(self.submission.speaker)

        if self.keynote_id:
            schedule_item_speakers.extend(
                speaker.user for speaker in self.keynote.speakers.all()
            )

        schedule_item_speakers.extend(
            speaker.user for speaker in self.additional_speakers.all()
        )

        for speaker in schedule_item_speakers:
            if speaker is None:
                continue

            speakers.append(
                ScheduleItemUser(
                    id=speaker.id,
                    fullname=speaker.fullname,
                    full_name=speaker.full_name,
                    participant=participants_data.get(speaker.id),
                )
            )

        return speakers

    @strawberry_django.field(select_related=["keynote"])
    def keynote(
        self, info: Info
    ) -> Annotated["Keynote", strawberry.lazy("api.conferences.types")] | None:
        return self.keynote if self.keynote_id else None

    rooms: list[Room]

    @strawberry.field
    def image(self, info: Info) -> str | None:
        if not self.image:
            return None

        return info.context.request.build_absolute_uri(self.image.url)

    @strawberry_django.field(name="slidoUrl", only=["slido_url", "slot_id"])
    def _slido_url(self, info: Info) -> str:
        if self.slido_url:
            return self.slido_url

        # For multi-room items we use the first room slido url
        return self.slot.day.added_rooms.get(room_id=self.rooms.first().id).slido_url
