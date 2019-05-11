import graphene
from graphene_django import DjangoObjectType

from users.types import UserType

from .models import Room, ScheduleItem


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        exclude_fields = ("id",)


class ModelScheduleItemType(DjangoObjectType):
    additional_speakers = graphene.NonNull(graphene.List(graphene.NonNull(UserType)))

    def resolve_additional_speakers(self, info):
        return self.additional_speakers.all()

    class Meta:
        model = ScheduleItem
        only_fields = (
            "id",
            "conference",
            "start",
            "end",
            "type",
            "rooms",
            "submission",
            "title",
            "description",
            "additional_speakers",
        )
