import strawberry
from graphql import GraphQLError

from .types import MeUser


@strawberry.type
class UsersQuery:
    @strawberry.field
    def me(self, info) -> MeUser:
        user = info.context["request"].user

        if not user.is_authenticated:
            raise GraphQLError("User not logged in")

        return user
