from schedule.api.mutations.book_schedule_item import book_schedule_item
from schedule.api.mutations.cancel_booking_schedule_item import (
    cancel_booking_schedule_item,
)
from schedule.api.mutations.change_schedule_item_slot import change_schedule_item_slot
from schedule.api.mutations.create_schedule_item import create_schedule_item
from schedule.api.mutations.create_schedule_slot import create_schedule_slot
from schedule.api.mutations.update_schedule_invitation import update_schedule_invitation
from schedule.api.mutations.unstar_schedule_item import unstar_schedule_item
from schedule.api.mutations.star_schedule_item import star_schedule_item
from schedule.api.queries.schedule_invitation import schedule_invitation
from schedule.api.queries.unassigned_schedule_items import unassigned_schedule_items
from schedule.api.queries.search_events_for_schedule import search_events_for_schedule


from strawberry.tools import create_type


ScheduleMutations = create_type(
    "ScheduleMutations",
    [
        book_schedule_item,
        cancel_booking_schedule_item,
        star_schedule_item,
        unstar_schedule_item,
        update_schedule_invitation,
        change_schedule_item_slot,
        create_schedule_item,
        create_schedule_slot,
    ],
)

ScheduleQuery = create_type(
    "ScheduleQuery",
    [
        schedule_invitation,
        unassigned_schedule_items,
        search_events_for_schedule,
    ],
)
