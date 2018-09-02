import graphene

from graphql import GraphQLError

from .types import MeUserType


class UsersQuery(graphene.AbstractType):
    me = graphene.Field(MeUserType)

    def resolve_me(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not logged in")
        else:
            return info.context.user
