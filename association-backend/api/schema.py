import strawberry

from api.mutation import Mutation
from api.query import Query
from api.types.user import User

schema = strawberry.federation.Schema(query=Query, mutation=Mutation, types=[User])
