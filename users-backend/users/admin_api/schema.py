import strawberry
from pythonit_toolkit.api.extensions import SentryExtension

from users.admin_api.mutation import Mutation
from users.admin_api.query import Query

schema = strawberry.federation.Schema(
    query=Query, mutation=Mutation, extensions=[SentryExtension]
)
