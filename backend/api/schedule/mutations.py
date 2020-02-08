import typing
from datetime import date, datetime, time, timedelta

import strawberry
from api.conferences.types import Day, ScheduleSlot
from api.helpers.ids import decode_hashid
from conferences.models import Conference
from schedule.models import Day as DayModel
from schedule.models import ScheduleItem, Slot
from strawberry.types.datetime import Date


@strawberry.type
class AddScheduleSlotError:
    message: str


def add_minutes_to_time(time: time, minutes: int) -> time:
    return (datetime.combine(date(1, 1, 1), time) + timedelta(minutes=minutes)).time()


@strawberry.type
class UpdateOrCreateSlotItemError:
    message: str


@strawberry.input
class UpdateOrCreateSlotItemInput:
    slot_id: strawberry.ID
    item_id: typing.Optional[strawberry.ID]
    submission_id: typing.Optional[strawberry.ID]
    title: typing.Optional[str]
    rooms: typing.List[strawberry.ID]


# TODO: permission
@strawberry.type
class ScheduleMutations:
    @strawberry.mutation
    def add_schedule_slot(
        self, info, conference: strawberry.ID, duration: int, day: Date
    ) -> typing.Union[AddScheduleSlotError, Day]:
        conference = Conference.objects.get(code=conference)
        day, _ = DayModel.objects.get_or_create(day=day, conference=conference)

        # TODO: ordering
        last_slot = day.slots.last()

        # TODO: is it ok to hardcode this?
        hour = time(8, 45)
        offset = 0

        if last_slot:
            hour = add_minutes_to_time(last_slot.hour, last_slot.duration)
            offset = last_slot.offset + last_slot.size

        Slot.objects.create(day=day, hour=hour, duration=duration, offset=offset)

        return Day(day=day.day, slots=day.slots.all())

    @strawberry.mutation
    def update_or_create_slot_item(
        self, info, input: UpdateOrCreateSlotItemInput
    ) -> typing.Union[UpdateOrCreateSlotItemError, ScheduleSlot]:
        # TODO: validate this is not none
        slot = Slot.objects.select_related("day").filter(id=input.slot_id).first()

        submission_id = (
            decode_hashid(input.submission_id) if input.submission_id else None
        )

        data = {
            "type": (
                ScheduleItem.TYPES.submission
                if submission_id
                else ScheduleItem.TYPES.custom
            ),
            "slot": slot,
            "submission_id": submission_id,
            "conference": slot.day.conference,
        }

        if input.title:
            data["title"] = input.title

        schedule_item, _ = ScheduleItem.objects.update_or_create(
            id=input.item_id, defaults=data
        )
        schedule_item.rooms.set(input.rooms)

        return ScheduleSlot(
            hour=slot.hour,
            duration=slot.duration,
            offset=slot.offset,
            size=slot.size,
            id=slot.id,
        )
