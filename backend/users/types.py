from graphene_django import DjangoObjectType

from .models import User


class MeUserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ("id", "email")
