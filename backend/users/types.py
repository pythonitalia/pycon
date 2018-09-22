from .models import User

import graphene

from graphene import ObjectType
from graphene_django import DjangoObjectType


class MeUserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ("id", "email")


class PaginatedUsersType(ObjectType):
    total_count = graphene.Int(required=True)
    objects = graphene.List(graphene.NonNull(MeUserType), required=True)
