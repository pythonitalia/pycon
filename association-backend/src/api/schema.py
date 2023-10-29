import strawberry
from pythonit_toolkit.api.extensions import SentryExtension

from src.api.query import Query

schema = strawberry.federation.Schema(query=Query, extensions=[SentryExtension])
