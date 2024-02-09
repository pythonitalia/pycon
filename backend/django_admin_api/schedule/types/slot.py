from datetime import time
from django_admin_api.schedule.types.schedule_item import ScheduleItem


import strawberry


@strawberry.type
class Slot:
    id: strawberry.ID
    hour: time
    duration: int
    type: str
    items: list[ScheduleItem]

    @classmethod
    def from_model(cls, slot):
        return cls(
            id=slot.id,
            hour=slot.hour,
            duration=slot.duration,
            type=slot.type,
            items=[ScheduleItem.from_model(item) for item in slot.items.all()],
        )
