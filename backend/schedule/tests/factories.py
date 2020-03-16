import factory
import factory.fuzzy
from conferences.tests.factories import ConferenceFactory
from factory.django import DjangoModelFactory
from languages.tests.factories import LanguageFactory
from pytest_factoryboy import register
from schedule.models import Day, Room, ScheduleItem, Slot, ScheduleItemBooking
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory


@register
class RoomFactory(DjangoModelFactory):
    name = factory.Faker("word")
    conference = factory.SubFactory(ConferenceFactory)

    class Meta:
        model = Room


@register
class DayFactory(DjangoModelFactory):
    day = factory.Faker("future_date")

    class Meta:
        model = Day


@register
class SlotFactory(DjangoModelFactory):
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

    maximum_capacity = 20

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        _type = kwargs.get("type", None)

        if _type == ScheduleItem.TYPES.custom:
            kwargs.pop("submission", None)

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
                self.rooms.add(RoomFactory(name=room, conference=self.conference))

    @factory.post_generation
    def additional_speakers(self, create, extracted, size=0, **kwargs):
        if not create:
            return

        self.additional_speakers.set(
            UserFactory.simple_generate_batch(create, size, **kwargs)
        )

    class Meta:
        model = ScheduleItem


@register
class ScheduleItemBookingFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    schedule_item = factory.SubFactory(ScheduleItemFactory)

    class Meta:
        model = ScheduleItemBooking
