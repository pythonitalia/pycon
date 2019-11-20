import random

import factory.fuzzy
from django.conf import settings
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from conferences.tests.factories import (
    AudienceLevelFactory,
    ConferenceFactory,
    DurationFactory,
    TopicFactory,
)
from languages.models import Language
from submissions.models import Submission, SubmissionTag, SubmissionType
from users.tests.factories import UserFactory


@register
class SubmissionTypeFactory(DjangoModelFactory):
    class Meta:
        model = SubmissionType
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(["talk", "tutorial"])


@register
class SubmissionTagFactory(DjangoModelFactory):
    class Meta:
        model = SubmissionTag
        django_get_or_create = ("name",)

    name = factory.Faker("word")


@register
class SubmissionFactory(DjangoModelFactory):
    class Meta:
        model = Submission

    conference = factory.SubFactory(ConferenceFactory)

    title = factory.Faker("sentence")
    abstract = factory.Faker("text")
    elevator_pitch = factory.Faker("text")
    notes = factory.Faker("text")
    type = factory.SubFactory(SubmissionTypeFactory)
    duration = factory.SubFactory(DurationFactory)
    speaker = factory.SubFactory(UserFactory)
    topic = factory.SubFactory(TopicFactory)
    audience_level = factory.SubFactory(AudienceLevelFactory)

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
        else:
            self.languages.add(
                Language.objects.get(code=random.choice(settings.LANGUAGES)[0])
            )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """Accept a list of tags and add them to the submission"""

        if not create:
            return

        if extracted:
            for tag_name in extracted:
                tag, _ = SubmissionTag.objects.get_or_create(name=tag_name)
                self.tags.add(tag)
        else:
            for _ in range(random.randint(1, 7)):
                self.tags.add(
                    SubmissionTag.objects.get_or_create(
                        name=factory.Faker("word").generate()
                    )[0]
                )
