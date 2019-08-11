import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from tests.conferences.factories import TicketFareFactory
from tests.orders.factories import OrderFactory
from tests.users.factories import UserFactory
from tickets import QUESTION_TYPE_CHOICE, QUESTION_TYPES
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

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        if kwargs["question"].question_type == QUESTION_TYPE_CHOICE:
            kwargs["answer"] = (
                factory.fuzzy.FuzzyChoice(kwargs["question"].choices.all())
                .fuzz()
                .choice
            )
        return super(UserAnswerFactory, cls)._create(model_class, *args, **kwargs)
