import strawberry
from pythonit_toolkit.api.extensions import SentryExtension

# from .mutation import Mutation


@strawberry.type
class Query:
    empty: str = "empty"


schema = strawberry.federation.Schema(
    Query,
    # Mutation,
    extensions=[SentryExtension],
)
