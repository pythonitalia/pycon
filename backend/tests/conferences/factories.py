import pytz
import factory
import factory.fuzzy

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from conferences.models import Conference, Topic, Deadline
from languages.models import Language


@register
class ConferenceFactory(DjangoModelFactory):
    name = factory.Faker('name')
    code = factory.Faker('text', max_nb_chars=10)

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
