from .models import User

from graphene_django import DjangoObjectType


class MeUserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ("id", "email")
