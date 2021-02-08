import strawberry

from users.admin_api.mutation import Mutation
from users.admin_api.query import Query

schema = strawberry.federation.Schema(query=Query, mutation=Mutation)
