import graphene

from graphql import GraphQLError

from api.settings import LIMIT_DEFAULT_VALUE
from api.pagination import get_pagination

from .types import MeUserType, PaginatedUsersType
from .models import User


class UsersQuery(graphene.AbstractType):
    me = graphene.Field(MeUserType)
    users = graphene.NonNull(
        PaginatedUsersType, offset=graphene.Int(), limit=graphene.Int()
    )

    def resolve_me(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not logged in")

        return info.context.user

    def resolve_users(self, info, offset, limit=LIMIT_DEFAULT_VALUE):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not logged in")

        if not info.context.user.is_superuser:
            raise GraphQLError("You don't have the permissions")

        return get_pagination(
            User.objects.all().order_by('-date_joined'),
            offset,
            limit,
            PaginatedUsersType
        )
