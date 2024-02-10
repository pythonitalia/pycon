from django_admin_api.permissions import CanEditSchedule
from django_admin_api.schedule.types.slot import Slot
from schedule.models import Room, ScheduleItem as ScheduleItemModel, Slot as SlotModel
import strawberry
from strawberry.types import Info
from custom_admin.audit import create_change_admin_log_entry
from django.db import transaction


@strawberry.input
class ChangeScheduleItemSlotInput:
    conference_id: strawberry.ID
    schedule_item_id: strawberry.ID
    new_slot_id: strawberry.ID
    rooms: list[strawberry.ID]


@strawberry.field(permission_classes=[CanEditSchedule])
def change_schedule_item_slot(
    info: Info, input: ChangeScheduleItemSlotInput
) -> list[Slot]:
    conference_id = input.conference_id

    new_slot = SlotModel.objects.for_conference(conference_id).get(id=input.new_slot_id)
    schedule_item = ScheduleItemModel.objects.for_conference(conference_id).get(
        id=input.schedule_item_id
    )

    old_slot = schedule_item.slot
    old_rooms_names = ",".join(schedule_item.rooms.values_list("name", flat=True))

    slot_changed = old_slot.id != new_slot.id
    rooms_changed = set(
        map(str, schedule_item.rooms.values_list("id", flat=True))
    ) != set(input.rooms)

    with transaction.atomic():
        schedule_item.rooms.set(input.rooms)
        schedule_item.slot_id = new_slot
        schedule_item.save(update_fields=["slot"])

        changes = []
        if slot_changed:
            changes.append(f"Changed Slot from {str(old_slot)} to {str(new_slot)}")

        if rooms_changed:
            new_rooms_names = ",".join(
                Room.objects.filter(id__in=input.rooms).values_list("name", flat=True)
            )
            changes.append(
                f"Changed Rooms from {str(old_rooms_names)} to {str(new_rooms_names)}"
            )

        create_change_admin_log_entry(
            info.context.request.user,
            schedule_item,
            " and ".join(changes),
        )

    updated_slots = [
        Slot.from_model(old_slot),
    ]

    if slot_changed:
        updated_slots.append(Slot.from_model(new_slot))

    return updated_slots
