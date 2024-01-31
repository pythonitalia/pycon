from datetime import date, time
from conferences.models.conference import Conference
import strawberry


@strawberry.type
class Room:
    id: strawberry.ID
    name: str

    @classmethod
    def from_model(cls, room):
        return cls(id=room.id, name=room.name)


@strawberry.type
class ScheduleItem:
    id: strawberry.ID
    title: str
    rooms: list[Room]

    @classmethod
    def from_model(cls, item):
        return cls(
            id=item.id,
            title=item.title,
            rooms=[Room.from_model(room) for room in item.rooms.all()],
        )


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


@strawberry.type
class Day:
    id: strawberry.ID
    day: date
    rooms: list[Room]
    slots: list[Slot]

    @classmethod
    def from_model(cls, day):
        return cls(
            id=day.day,
            day=day.day,
            rooms=[
                Room.from_model(added_room.room) for added_room in day.added_rooms.all()
            ],
            slots=[Slot.from_model(slot) for slot in day.slots.all()],
        )


@strawberry.type
class Schedule:
    id: strawberry.ID
    days: list[Day]

    @classmethod
    def from_model(cls, conference: Conference) -> "Schedule":
        return cls(
            id=conference.id,
            days=[Day.from_model(day) for day in conference.days.all()],
        )


@strawberry.field
def conference_schedule(conference_id: strawberry.ID) -> Schedule:
    conference = Conference.objects.get(id=conference_id)
    return Schedule.from_model(conference)
