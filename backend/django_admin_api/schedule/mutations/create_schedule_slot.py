from custom_admin.audit import create_addition_admin_log_entry
from django.db import transaction
from django_admin_api.schedule.types.day import Day
from datetime import time, timedelta, datetime
from schedule.models import Day as DayModel, Slot as SlotModel
import strawberry
from django_admin_api.permissions import CanEditSchedule


@strawberry.input
class CreateScheduleSlotInput:
    conference_id: strawberry.ID
    day_id: strawberry.ID
    duration: int
    type: str


@strawberry.field(permission_classes=[CanEditSchedule])
def create_schedule_slot(info, input: CreateScheduleSlotInput) -> Day:
    conference_id = input.conference_id
    day = DayModel.objects.for_conference(conference_id).get(id=input.day_id)

    with transaction.atomic():
        previous_slot = day.slots.order_by("hour").last()
        hour = (
            (
                datetime.combine(day.day, previous_slot.hour)
                + timedelta(minutes=previous_slot.duration)
            ).time()
            if previous_slot
            else time(9, 15)
        )

        SlotModel.objects.create(
            day=day,
            hour=hour,
            duration=input.duration,
            type=input.type,
        )

        create_addition_admin_log_entry(
            user=info.context.request.user,
            obj=day,
            change_message=f"Created Slot {hour} [{input.duration}]",
        )

    refreshed_day = DayModel.objects.for_conference(conference_id).get(id=input.day_id)
    return Day.from_model(refreshed_day)
