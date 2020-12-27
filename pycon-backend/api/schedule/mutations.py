import typing
from datetime import date, datetime, time, timedelta

import strawberry
from api.conferences.types import Day, ScheduleSlot
from api.helpers.ids import decode_hashid
from conferences.models import Conference
from languages.models import Language
from schedule.models import Day as DayModel
from schedule.models import ScheduleItem, Slot
from submissions.models import Submission

from ..permissions import IsStaffPermission


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
    rooms: typing.List[strawberry.ID]
    title: typing.Optional[str] = None
    item_id: typing.Optional[strawberry.ID] = None
    submission_id: typing.Optional[strawberry.ID] = None


@strawberry.type
class UpdateOrCreateSlotItemResult:
    updated_slots: typing.List[ScheduleSlot]


@strawberry.type
class ScheduleMutations:
    @strawberry.mutation(permission_classes=[IsStaffPermission])
    def add_schedule_slot(
        self, info, conference: strawberry.ID, duration: int, day: date
    ) -> typing.Union[AddScheduleSlotError, Day]:
        conference = Conference.objects.get(code=conference)
        day, _ = DayModel.objects.get_or_create(day=day, conference=conference)

        last_slot = day.slots.last()

        hour = (
            add_minutes_to_time(last_slot.hour, last_slot.duration)
            if last_slot
            else time(8, 30)
        )

        Slot.objects.create(day=day, hour=hour, duration=duration)

        return Day.from_db(day)

    @strawberry.mutation(permission_classes=[IsStaffPermission])
    def update_or_create_slot_item(
        self, info, input: UpdateOrCreateSlotItemInput
    ) -> typing.Union[UpdateOrCreateSlotItemError, UpdateOrCreateSlotItemResult]:
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

        updated_slots: typing.List[ScheduleSlot] = []

        if input.item_id:
            schedule_item = ScheduleItem.objects.select_related("slot").get(
                id=input.item_id
            )
            updated_slots.append(
                ScheduleSlot(
                    hour=schedule_item.slot.hour,
                    duration=schedule_item.slot.duration,
                    id=schedule_item.slot.id,
                )
            )

            # make sure we keep the same type and submission
            data["submission_id"] = schedule_item.submission_id
            data["type"] = schedule_item.type

            ScheduleItem.objects.filter(id=input.item_id).update(**data)
        else:
            language_code = "en"

            if submission_id:
                language_code = (
                    Submission.objects.filter(id=submission_id)
                    .values_list("languages__code", flat=True)
                    .order_by("languages__code")
                    .first()
                )

            data["language"] = Language.objects.get(code=language_code)

            schedule_item = ScheduleItem.objects.create(**data)

        schedule_item.rooms.set(input.rooms)

        updated_slots.append(
            ScheduleSlot(hour=slot.hour, duration=slot.duration, id=slot.id)
        )

        return UpdateOrCreateSlotItemResult(updated_slots=updated_slots)
