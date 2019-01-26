import pytz
import factory
import factory.fuzzy

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from schedule.models import ScheduleItem

from tests.conferences.factories import ConferenceFactory, TopicFactory
from tests.submissions.factories import SubmissionFactory


@register
class ScheduleItemFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    submission = factory.SubFactory(SubmissionFactory)
    topic = factory.SubFactory(TopicFactory)

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

    class Meta:
        model = ScheduleItem
