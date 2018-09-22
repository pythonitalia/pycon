import graphene

from graphene import ObjectType
from graphene_django import DjangoObjectType

from .models import User


class MeUserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ("id", "email")


class PaginatedUsersType(ObjectType):
    total_count = graphene.Int(required=True)
    objects = graphene.List(graphene.NonNull(MeUserType), required=True)
