import factory
import factory.fuzzy
import pytz
from conferences.models import AudienceLevel, Conference, Deadline, Duration, Topic
from django.utils import timezone
from factory.django import DjangoModelFactory
from i18n.tests.factories import LanguageFactory
from languages.models import Language
from pytest_factoryboy import register
from submissions.models import SubmissionType


@register
class ConferenceFactory(DjangoModelFactory):
    name = LanguageFactory("name")
    code = factory.Faker("text", max_nb_chars=10)
    introduction = LanguageFactory("sentence")

    start = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    end = factory.Faker("future_datetime", tzinfo=pytz.UTC)

    timezone = pytz.timezone("Europe/Rome")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        specified_deadlines = {}

        for deadline in Deadline.TYPES:
            _type = deadline[0]

            value = kwargs.pop(f"active_{_type}", None)
            specified_deadlines[_type] = value

        instance = super()._create(model_class, *args, **kwargs)

        for _type, value in specified_deadlines.items():
            if value is True:
                instance.deadlines.add(DeadlineFactory(conference=instance, type=_type))
            elif value is False:
                instance.deadlines.add(
                    DeadlineFactory(
                        conference=instance,
                        type=_type,
                        start=timezone.now() - timezone.timedelta(days=10),
                        end=timezone.now() - timezone.timedelta(days=5),
                    )
                )

        return instance

    @factory.post_generation
    def topics(self, create, extracted, **kwargs):
        """Accepts a list of topic names and adds each topic to the
        Conference allowed submission topics.

        If a topic with that name doesn't exists, a new one is created.

        This fixture makes easier to add allowed topics to a Conference in the tests
        """
        if not create:
            return

        if extracted:
            for topic in extracted:
                self.topics.add(Topic.objects.get_or_create(name=topic)[0])

    @factory.post_generation
    def languages(self, create, extracted, **kwargs):
        """Accepts a list of language codes and adds each language to the
        Conference allowed languages.

        This fixture makes easier to add allowed languages to a Conference in the tests
        """
        if not create:
            return

        if extracted:
            for language_code in extracted:
                self.languages.add(Language.objects.get(code=language_code))

    @factory.post_generation
    def submission_types(self, create, extracted, **kwargs):
        """Accepts a list of submission type names and adds
        each submission type to the Conference allowed submission types.

        If a submission type with that name doesn't exists, a new one is created.

        This fixture makes easier to add allowed submission types
        to a Conference in the tests
        """
        if not create:
            return

        if extracted:
            for submission_type in extracted:
                self.submission_types.add(
                    SubmissionType.objects.get_or_create(name=submission_type)[0]
                )

    @factory.post_generation
    def durations(self, create, extracted, **kwargs):
        """Accepts a list of durations (in minutes) and creates a duration object to the
        Conference allowed durations.

        This fixture makes easier to add durations to a Conference in the tests
        """
        if not create:
            return

        if extracted:
            for duration in extracted:
                duration, created = Duration.objects.get_or_create(
                    duration=duration,
                    conference=self,
                    defaults={"name": f"{duration}m"},
                )

                if created:
                    duration.allowed_submission_types.set(SubmissionType.objects.all())

                self.durations.add(duration)

    @factory.post_generation
    def audience_levels(self, create, extracted, **kwargs):

        if not create:
            return

        if extracted:
            for audience_level in extracted:
                self.audience_levels.add(
                    AudienceLevel.objects.get_or_create(name=audience_level)[0]
                )

    class Meta:
        model = Conference
        django_get_or_create = ("code",)


@register
class TopicFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Topic
        django_get_or_create = ("name",)


@register
class DeadlineFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    type = factory.fuzzy.FuzzyChoice([deadline[0] for deadline in Deadline.TYPES])
    name = LanguageFactory("sentence")
    description = LanguageFactory("sentence")

    start = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    end = factory.Faker("future_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = Deadline


@register
class AudienceLevelFactory(DjangoModelFactory):
    name = factory.fuzzy.FuzzyChoice(("Beginner", "Intermidiate", "Advanced"))

    class Meta:
        model = AudienceLevel
        django_get_or_create = ("name",)


@register
class DurationFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)

    name = factory.Faker("word")
    duration = factory.Faker("pyint")
    notes = factory.Faker("text")

    class Meta:
        model = Duration
