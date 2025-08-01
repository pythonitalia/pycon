import random

import factory.fuzzy
from django.conf import settings
from factory.django import DjangoModelFactory

from conferences.tests.factories import (
    AudienceLevelFactory,
    ConferenceFactory,
    DurationFactory,
    TopicFactory,
)
from i18n.tests.factories import LanguageFactory
from languages.models import Language
from users.tests.factories import UserFactory
from submissions.models import (
    Submission,
    SubmissionComment,
    SubmissionTag,
    SubmissionType,
    ProposalMaterial,
)


class SubmissionTypeFactory(DjangoModelFactory):
    class Meta:
        model = SubmissionType
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(["talk", "tutorial"])


class SubmissionTagFactory(DjangoModelFactory):
    class Meta:
        model = SubmissionTag
        django_get_or_create = ("name",)

    name = factory.Faker("word")


class SubmissionFactory(DjangoModelFactory):
    class Meta:
        model = Submission

    conference = factory.SubFactory(ConferenceFactory)

    title = LanguageFactory("sentence")
    abstract = LanguageFactory("text")
    elevator_pitch = LanguageFactory("text")
    notes = factory.Faker("text")
    type = factory.SubFactory(SubmissionTypeFactory)
    speaker = factory.SubFactory(UserFactory)
    duration = factory.SubFactory(DurationFactory)
    topic = factory.SubFactory(TopicFactory)
    audience_level = factory.SubFactory(AudienceLevelFactory)
    speaker_level = factory.fuzzy.FuzzyChoice(
        Submission.SPEAKER_LEVELS, getter=lambda c: c[0]
    )
    previous_talk_video = factory.Faker("url")
    status = "proposed"

    @factory.post_generation
    def custom_submission_type(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.type = self.conference.submission_types.get(name=extracted)

    @factory.post_generation
    def custom_audience_level(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.audience_level = self.conference.audience_levels.get(name=extracted)

    @factory.post_generation
    def custom_duration(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.duration = self.conference.durations.get(name=extracted)

    @factory.post_generation
    def custom_topic(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.topic = self.conference.topics.get(name=extracted)

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

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        if create and results:
            obj.save()


class AcceptedSubmissionFactory(SubmissionFactory):
    status = "accepted"


class SubmissionCommentFactory(DjangoModelFactory):
    class Meta:
        model = SubmissionComment

    submission = factory.SubFactory(SubmissionFactory)
    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)


class ProposalMaterialFactory(DjangoModelFactory):
    class Meta:
        model = ProposalMaterial

    proposal = factory.SubFactory(SubmissionFactory)
