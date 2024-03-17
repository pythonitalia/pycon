from languages.models import Language
from users.tests.factories import UserFactory

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from languages.tests.factories import LanguageFactory
from schedule.models import (
    Day,
    Room,
    ScheduleItem,
    ScheduleItemAdditionalSpeaker,
    ScheduleItemAttendee,
    ScheduleItemSentForVideoUpload,
    Slot,
)
from submissions.tests.factories import SubmissionFactory


@register
class RoomFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Room


@register
class DayFactory(DjangoModelFactory):
    day = factory.Faker("future_date")

    class Meta:
        model = Day


@register
class SlotFactory(DjangoModelFactory):
    day = factory.SubFactory(DayFactory)

    class Meta:
        model = Slot


@register
class ScheduleItemFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    submission = factory.SubFactory(SubmissionFactory)
    language = factory.SubFactory(LanguageFactory)
    title = factory.Faker("text", max_nb_chars=100)
    slug = factory.Faker("slug")
    description = factory.Faker("text")
    type = factory.fuzzy.FuzzyChoice(["submission", "custom"])
    image = factory.django.ImageField()

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        _type = kwargs.get("type", None)
        if _type == ScheduleItem.TYPES.custom:
            kwargs.pop("submission", None)

        _language = kwargs.get("language", None)
        if not _language:
            kwargs["language"] = Language.objects.get(code="en")
        elif isinstance(_language, str):
            kwargs["language"] = Language.objects.get(code=_language)

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

    @factory.post_generation
    def additional_speakers(self, create, extracted=0, **kwargs):
        if not create:
            return

        size = extracted or 0
        self.additional_speakers.set(
            ScheduleItemAdditionalSpeakerFactory.simple_generate_batch(
                create, size, **kwargs
            )
        )

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        if create and results:
            obj.save()

    class Meta:
        model = ScheduleItem


@register
class ScheduleItemAdditionalSpeakerFactory(DjangoModelFactory):
    scheduleitem = factory.SubFactory(ScheduleItemFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = ScheduleItemAdditionalSpeaker


@register
class ScheduleItemAttendeeFactory(DjangoModelFactory):
    schedule_item = factory.SubFactory(ScheduleItemFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = ScheduleItemAttendee


@register
class ScheduleItemSentForVideoUploadFactory(DjangoModelFactory):
    schedule_item = factory.SubFactory(ScheduleItemFactory)

    class Meta:
        model = ScheduleItemSentForVideoUpload
