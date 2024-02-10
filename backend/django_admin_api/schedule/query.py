from django_admin_api.schedule.queries.search_events import search_events
from django_admin_api.schedule.queries.unassigned_schedule_items import (
    unassigned_schedule_items,
)
from strawberry.tools import create_type
from django_admin_api.schedule.queries.conference_schedule import conference_schedule

ScheduleQuery = create_type(
    "ScheduleQuery", [conference_schedule, search_events, unassigned_schedule_items]
)
