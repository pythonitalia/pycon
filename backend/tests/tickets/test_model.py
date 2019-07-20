import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from tests.tickets.factories import TicketFactory, TicketQuestionFactory, TicketQuestionChoiceFactory, UserAnswerFactory
from tickets import QUESTION_TYPE_CHOICE, QUESTION_TYPE_TEXT
from tickets.models import UserAnswer


@mark.django_db
def test_ticket_text_answer():
    ticket = TicketFactory()
    question = TicketQuestionFactory(question_type=QUESTION_TYPE_TEXT)

    answer = UserAnswerFactory(ticket=ticket, question=question)

    assert answer.answer


@mark.django_db
def test_ticket_choice_answer():
    ticket = TicketFactory()
    question = TicketQuestionFactory(question_type=QUESTION_TYPE_CHOICE)
    choices = [
        TicketQuestionChoiceFactory(question=question),
        TicketQuestionChoiceFactory(question=question),
    ]
    ticket.ticket_fare.questions.add(question)

    answer = UserAnswerFactory(ticket=ticket, question=question)

    assert answer.answer in [choice.choice for choice in choices]


@mark.django_db
def test_ticket_choice_answer_wrong_data():
    ticket = TicketFactory()
    question = TicketQuestionFactory(question_type=QUESTION_TYPE_CHOICE)
    TicketQuestionChoiceFactory(question=question),
    TicketQuestionChoiceFactory(question=question),
    ticket.ticket_fare.questions.add(question)

    other_question = TicketQuestionFactory(question_type=QUESTION_TYPE_CHOICE)
    wrong_choice = TicketQuestionChoiceFactory(question=other_question)
    ticket.ticket_fare.questions.add(other_question)

    with pytest.raises(ValidationError):
        UserAnswer.objects.create(
            ticket=ticket,
            question=question,
            answer=wrong_choice.choice
        )
