import strawberry
from pythonit_toolkit.api.extensions import SentryExtension

from admin_api.types.user import User
from src.admin_api.query import Query

schema = strawberry.federation.Schema(
    query=Query, extensions=[SentryExtension], types=[User]
)
