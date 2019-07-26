import strawberry
from graphql import GraphQLError

from .types import MeUserType


@strawberry.type
class UsersQuery:
    @strawberry.field
    def me(self, info) -> MeUserType:
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not logged in")

        return info.context.user
