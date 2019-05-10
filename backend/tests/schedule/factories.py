import pytz
import factory
import factory.fuzzy

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from schedule.models import ScheduleItem, Room

from tests.conferences.factories import ConferenceFactory
from tests.submissions.factories import SubmissionFactory


@register
class RoomFactory(DjangoModelFactory):
    name = factory.Faker('text', max_nb_chars=100)
    conference = factory.SubFactory(ConferenceFactory)

    class Meta:
        model = Room


@register
class ScheduleItemFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    submission = factory.SubFactory(SubmissionFactory)

    start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    end = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    title = factory.Faker('text', max_nb_chars=100)
    description = factory.Faker('text')
    type = factory.fuzzy.FuzzyChoice(['submission', 'custom'])

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        _type = kwargs.get('type', None)

        if _type == ScheduleItem.TYPES.custom:
            kwargs.pop('submission', None)

        return super()._create(model_class, *args, **kwargs)

    @factory.post_generation
    def rooms(self, create, extracted, **kwargs):
        """
        Convenience post_generator that adds the rooms passed
        as argument to the M2M `rooms` of the Schedule Item
        """
        if not create:
            return

        if extracted:
            for room in extracted:
                self.rooms.add(room)

    class Meta:
        model = ScheduleItem
