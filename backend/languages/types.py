from graphene_django import DjangoObjectType

from .models import Language


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language
        only_fields = ('id', 'code', 'name',)
