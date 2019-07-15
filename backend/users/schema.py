import graphene
from graphql import GraphQLError

from .types import MeUserType


class UsersQuery:
    me = graphene.Field(MeUserType)

    def resolve_me(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not logged in")

        return info.context.user
