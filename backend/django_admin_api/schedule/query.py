from strawberry.tools import create_type
from django_admin_api.schedule.queries.conference_schedule import conference_schedule

ScheduleQuery = create_type("ScheduleQuery", [conference_schedule])
