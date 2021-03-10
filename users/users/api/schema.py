import strawberry

from .mutation import Mutation
from .query import Query

schema = strawberry.federation.Schema(Query, Mutation)
