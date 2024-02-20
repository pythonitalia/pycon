from api.context import Info
from schedule.models import ScheduleItem as ScheduleItemModel
from api.schedule.types.schedule_item import ScheduleItem
from django.utils import timezone
from datetime import date, timedelta
from api.schedule.types.day_room import DayRoom
from api.schedule.types.slot import ScheduleSlot
import strawberry


@strawberry.type
class Day:
    id: strawberry.ID
    day: date

    @strawberry.field
    def random_events(self, limit: int = 4) -> list[ScheduleItem]:
        if limit > 10:
            raise ValueError("Limit cannot be greater than 10")

        return ScheduleItemModel.objects.filter(
            slot__day=self,
            type__in=[
                ScheduleItemModel.TYPES.talk,
                ScheduleItemModel.TYPES.training,
                ScheduleItemModel.TYPES.panel,
            ],
        ).order_by("?")[:limit]

    @strawberry.field
    def slots(
        self, info: Info, room: strawberry.ID | None = None
    ) -> list[ScheduleSlot]:
        if room:
            return list(self.slots.filter(items__rooms__id=room))
        return list(self.slots.all())

    @strawberry.field
    def running_events(self, info) -> list[ScheduleItem]:
        current_slot = self.slots.filter(
            hour__lte=timezone.now().astimezone(self.conference.timezone)
        ).last()

        if not current_slot:
            return []

        items = list(current_slot.items.all())
        if len(items) == 1:
            first_item = items[0]
            if first_item.rooms.first().name.lower() == "recruiting":
                current_slot = self.slots.filter(
                    hour__lte=timezone.now().astimezone(self.conference.timezone)
                    - timedelta(minutes=current_slot.duration)
                ).last()

        return [item for item in current_slot.items.all()]

    @strawberry.field
    def rooms(self) -> list[DayRoom]:
        added_rooms = self.added_rooms.all()
        return [
            DayRoom(
                id=added_room.room.id,
                name=added_room.room.name,
                type=added_room.room.type,
                streaming_url=added_room.streaming_url,
                slido_url=added_room.slido_url,
            )
            for added_room in added_rooms
        ]

    @classmethod
    def from_db(cls, instance):
        obj = cls(id=instance.id, day=instance.day)
        obj.slots = instance.slots
        obj.added_rooms = instance.added_rooms
        return obj
