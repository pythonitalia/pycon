from django_admin_api.schedule.mutation import ScheduleMutation
import strawberry
from strawberry.tools import merge_types

from django_admin_api.schedule.query import ScheduleQuery

Query = merge_types("Query", (ScheduleQuery,))
Mutation = merge_types("Mutation", (ScheduleMutation,))

schema = strawberry.Schema(query=Query, mutation=Mutation)
