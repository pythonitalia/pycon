import strawberry
from pythonit_toolkit.api.extensions import SentryExtension

from src.api.mutation import Mutation
from src.api.query import Query
from src.api.types.user import User

schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=[User],
    extensions=[SentryExtension],
    enable_federation_2=True,
)
