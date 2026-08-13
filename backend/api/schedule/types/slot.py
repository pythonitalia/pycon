from enum import Enum
from datetime import datetime, time, timedelta

from django.utils import timezone

from api.context import Info
from api.schedule.types.schedule_item import ScheduleItem


import strawberry
import strawberry_django
from schedule import models
from strawberry import auto


@strawberry.enum
class ScheduleSlotType(Enum):
    DEFAULT = "default"
    FREE_TIME = "free_time"
    BREAK = "break"


@strawberry_django.type(models.Slot)
class ScheduleSlot:
    id: auto
    hour: auto
    duration: auto
    type: ScheduleSlotType

    @strawberry.field
    def is_live(self) -> bool:
        with timezone.override(self.day.conference.timezone):
            now = timezone.localtime(timezone.now())
            end = (
                datetime.combine(now, self.hour) + timedelta(minutes=self.duration)
            ).time()
            return self.hour < now.time() < end

    @strawberry.field
    def end_hour(self) -> time:
        return (
            datetime.combine(timezone.datetime.today(), self.hour)
            + timedelta(minutes=self.duration)
        ).time()

    @strawberry.field
    def items(self, info: Info) -> list[ScheduleItem]:
        return self.items.all()
