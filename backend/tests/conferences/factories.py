import pytz
import factory
import factory.fuzzy

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from django.utils import timezone

from conferences.models import Conference, Topic, Deadline, AudienceLevel, Duration
from languages.models import Language
from submissions.models import SubmissionType


@register
class ConferenceFactory(DjangoModelFactory):
    name = factory.Faker('name')
    code = factory.Faker('text', max_nb_chars=10)

    start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    end = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # if the user specifies active_cfp (for example) we will create a deadline to the conference
        # if the value is True, we will create an active CFP (now is between start and end)
        # if the value is False, we will create a CFP with dates in the past
        specified_deadlines = {}

        for deadline in Deadline.TYPES:
            type = deadline[0]

            value = kwargs.pop(f'active_{type}', None)
            specified_deadlines[type] = value

        instance = super()._create(model_class, *args, **kwargs)

        for type, value in specified_deadlines.items():
            if value is True:
                instance.deadlines.add(DeadlineFactory(conference=instance, type=type))
            elif value is False:
                instance.deadlines.add(DeadlineFactory(
                    conference=instance,
                    type=type,
                    start=timezone.now() - timezone.timedelta(days=10),
                    end=timezone.now() - timezone.timedelta(days=5),
                ))

        return instance

    @factory.post_generation
    def topics(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for topic in extracted:
                self.topics.add(Topic.objects.get_or_create(name=topic)[0])

    @factory.post_generation
    def languages(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for language_code in extracted:
                self.languages.add(Language.objects.get(code=language_code))

    @factory.post_generation
    def submission_types(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for submission_type in extracted:
                self.submission_types.add(SubmissionType.objects.get_or_create(name=submission_type)[0])

    class Meta:
        model = Conference


@register
class TopicFactory(DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = Topic
        django_get_or_create = ('name',)


@register
class DeadlineFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    type = factory.fuzzy.FuzzyChoice([deadline[0] for deadline in Deadline.TYPES])

    start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    end = factory.Faker('future_datetime', tzinfo=pytz.UTC)

    class Meta:
        model = Deadline


@register
class AudienceLevelFactory(DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = AudienceLevel
        django_get_or_create = ('name', )


@register
class DurationFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)

    name = factory.Faker('word')
    duration = factory.Faker('pyint')
    notes = factory.Faker('text')

    class Meta:
        model = Duration
