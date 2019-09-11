import factory.fuzzy
from conferences.models import TicketFareQuestion
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from tests.conferences.factories import TicketFareFactory
from tests.orders.factories import OrderFactory
from tests.users.factories import UserFactory
from tickets import QUESTION_TYPES
from tickets.models import Ticket, TicketQuestion, TicketQuestionChoice, UserAnswer


@register
class TicketFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ticket_fare = factory.SubFactory(TicketFareFactory)
    order = factory.SubFactory(OrderFactory)

    class Meta:
        model = Ticket


@register
class TicketQuestionFactory(DjangoModelFactory):
    text = factory.Faker("sentence")
    question_type = factory.fuzzy.FuzzyChoice([v[0] for v in QUESTION_TYPES])

    @factory.post_generation
    def num_choices(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for i in range(0, extracted):
                self.choices.add(TicketQuestionChoiceFactory(question=self))

    @factory.post_generation
    def choices(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for t in extracted:
                TicketQuestionChoiceFactory(question=self, choice=t).save()

    class Meta:
        model = TicketQuestion


@register
class TicketQuestionChoiceFactory(DjangoModelFactory):
    question = factory.SubFactory(TicketQuestionFactory)
    choice = factory.Faker("text")

    class Meta:
        model = TicketQuestionChoice


@register
class UserAnswerFactory(DjangoModelFactory):
    ticket = factory.SubFactory(TicketFactory)
    question = factory.SubFactory(TicketQuestionFactory)
    answer = factory.Faker("text")

    class Meta:
        model = UserAnswer


@register
class TicketFareQuestionFactory(DjangoModelFactory):
    ticket_fare = factory.SubFactory(TicketFareFactory)
    question = factory.SubFactory(TicketQuestionFactory)
    is_required = factory.Faker("pybool")

    class Meta:
        model = TicketFareQuestion
