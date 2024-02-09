from django_admin_api.schedule.mutations.create_schedule_item import (
    create_schedule_item,
)
from strawberry.tools import create_type
from django_admin_api.schedule.mutations.change_schedule_item_slot import (
    change_schedule_item_slot,
)

ScheduleMutation = create_type(
    "ScheduleMutation",
    [change_schedule_item_slot, create_schedule_item],
)
