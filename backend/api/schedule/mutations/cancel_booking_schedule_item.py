from api.schedule.mutations.book_schedule_item import ScheduleItemNotBookable
from api.schedule.types import (
    ScheduleItem as ScheduleItemType,
)
from typing import Annotated, Union
import strawberry
from api.permissions import IsAuthenticated
from schedule.models import (
    ScheduleItem,
    ScheduleItemAttendee,
)


@strawberry.type
class UserIsNotBooked:
    message: str = "You are not booked for this event"


CancelBookingScheduleItemResult = Annotated[
    Union[ScheduleItemType, UserIsNotBooked, ScheduleItemNotBookable],
    strawberry.union(name="CancelBookingScheduleItemResult"),
]


@strawberry.mutation(permission_classes=[IsAuthenticated])
def cancel_booking_schedule_item(
    self, info, id: strawberry.ID
) -> CancelBookingScheduleItemResult:
    schedule_item = ScheduleItem.objects.get(id=id)
    user_id = info.context.request.user.id

    if schedule_item.attendees_total_capacity is None:
        return ScheduleItemNotBookable()

    if not schedule_item.attendees.filter(user_id=user_id).exists():
        return UserIsNotBooked()

    ScheduleItemAttendee.objects.filter(
        schedule_item=schedule_item, user_id=user_id
    ).delete()
    schedule_item.__strawberry_definition__ = ScheduleItemType.__strawberry_definition__
    return schedule_item
