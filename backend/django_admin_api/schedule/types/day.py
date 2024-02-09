from datetime import date
from django_admin_api.schedule.types.room import Room
from django_admin_api.schedule.types.slot import Slot
import strawberry


@strawberry.type
class Day:
    id: strawberry.ID
    day: date
    rooms: list[Room]
    slots: list[Slot]

    @classmethod
    def from_model(cls, day):
        return cls(
            id=day.id,
            day=day.day,
            rooms=[
                Room.from_model(added_room.room) for added_room in day.added_rooms.all()
            ],
            slots=[Slot.from_model(slot) for slot in day.slots.all()],
        )
