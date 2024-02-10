from enum import Enum
from django.db.models import Case, When, Value, IntegerField
from schedule.models import ScheduleItem as ScheduleItemModel
from django.utils import timezone
from datetime import datetime, time, timedelta
from api.schedule.types.schedule_item import ScheduleItem


import strawberry


@strawberry.enum
class ScheduleSlotType(Enum):
    DEFAULT = "default"
    FREE_TIME = "free_time"
    BREAK = "break"


@strawberry.type
class ScheduleSlot:
    hour: time
    duration: int
    type: ScheduleSlotType
    id: strawberry.ID

    @strawberry.field
    def is_live(self) -> bool:
        with timezone.override(self.day.conference.timezone):
            now = timezone.localtime(timezone.now())
            end = (
                datetime.combine(now, self.hour) + timedelta(minutes=self.duration)
            ).time()
            return self.hour < now.time() < end

    @strawberry.field
    def end_hour(self, info) -> time:
        return (
            datetime.combine(timezone.datetime.today(), self.hour)
            + timedelta(minutes=self.duration)
        ).time()

    @strawberry.field
    def items(self, info) -> list[ScheduleItem]:
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
