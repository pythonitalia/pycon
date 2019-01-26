from graphene_django import DjangoObjectType

from .models import ScheduleItem


class ModelScheduleItemType(DjangoObjectType):
    class Meta:
        model = ScheduleItem
        only_fields = (
            'id',
            'conference',
            'start',
            'end',
            'type',
            'topic',
            'submission',
            'title',
            'description'
        )
