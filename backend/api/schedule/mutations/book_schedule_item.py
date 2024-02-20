from typing import Annotated, Union
from pretix import user_has_admission_ticket
import strawberry
from api.permissions import IsAuthenticated
from schedule.models import (
    ScheduleItem,
    ScheduleItemAttendee,
)
from api.schedule.types import (
    ScheduleItem as ScheduleItemType,
)


@strawberry.type
class ScheduleItemIsFull:
    message: str = "This event is full"


@strawberry.type
class ScheduleItemNotBookable:
    message: str = "This event does not require booking"


@strawberry.type
class UserNeedsConferenceTicket:
    message: str = "You need to buy a ticket"


@strawberry.type
class UserIsAlreadyBooked:
    message: str = "You are already booked for this event"


BookScheduleItemResult = Annotated[
    Union[
        ScheduleItemType,
        ScheduleItemIsFull,
        UserNeedsConferenceTicket,
        UserIsAlreadyBooked,
        ScheduleItemNotBookable,
    ],
    strawberry.union(name="BookScheduleItemResult"),
]


@strawberry.mutation(permission_classes=[IsAuthenticated])
def book_schedule_item(info, id: strawberry.ID) -> BookScheduleItemResult:
    schedule_item = ScheduleItem.objects.get(id=id)
    user_id = info.context.request.user.id

    if not user_has_admission_ticket(
        email=info.context.request.user.email,
        event_organizer=schedule_item.conference.pretix_organizer_id,
        event_slug=schedule_item.conference.pretix_event_id,
    ):
        return UserNeedsConferenceTicket()

    if schedule_item.attendees_total_capacity is None:
        return ScheduleItemNotBookable()

    if schedule_item.attendees.filter(user_id=user_id).exists():
        return UserIsAlreadyBooked()

    if schedule_item.attendees.count() >= schedule_item.attendees_total_capacity:
        return ScheduleItemIsFull()

    ScheduleItemAttendee.objects.create(schedule_item=schedule_item, user_id=user_id)
    schedule_item.__strawberry_definition__ = ScheduleItemType.__strawberry_definition__
    return schedule_item
