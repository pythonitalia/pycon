from graphene_django import DjangoObjectType

from .models import Room, ScheduleItem


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        exclude_fields = ("id",)


class ModelScheduleItemType(DjangoObjectType):
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
