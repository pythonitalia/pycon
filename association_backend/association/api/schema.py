import strawberry
from association.api.mutation import Mutation
from association.api.query import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
