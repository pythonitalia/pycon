import strawberry
from strawberry.tools import merge_types

from django_admin_api.schedule.query import ScheduleQuery

Query = merge_types("Query", (ScheduleQuery,))

schema = strawberry.Schema(query=Query)
