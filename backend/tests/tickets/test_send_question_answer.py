from pytest import mark
from tickets.models import UserAnswer


def _submit_answer(graphql_client, ticket, question, answer):
    return graphql_client.query(
        """
    mutation($ticket: ID!, $question: ID!, $answer: String!) {
        sendQuestionAnswer(input: {
            ticket: $ticket,
            question: $question,
            answer: $answer
        }) {
            __typename

            ... on UserAnswer {
                answer
            }

            ... on SendQuestionAnswerErrors {
                validationTicket: ticket
                validationQuestion: question
                validationAnswer: answer
                nonFieldErrors
            }
        }
    }
    """,
        variables={"ticket": ticket.id, "question": question.id, "answer": answer},
    )


@mark.django_db
def test_answer_text_question(
    graphql_client, user, ticket_factory, ticket_fare_question_factory
):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)
    question = ticket_fare_question_factory(
        ticket_fare=ticket.ticket_fare, question__question_type="text"
    )

    response = _submit_answer(graphql_client, ticket, question.question, "test")

    assert response["data"]["sendQuestionAnswer"]["__typename"] == "UserAnswer"
    assert response["data"]["sendQuestionAnswer"]["answer"] == "test"


@mark.django_db
def test_previous_answer_gets_replaced_when_sending_a_new_one(
    graphql_client, user, ticket_factory, ticket_fare_question_factory
):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)
    question = ticket_fare_question_factory(
        ticket_fare=ticket.ticket_fare, question__question_type="text"
    )

    response = _submit_answer(graphql_client, ticket, question.question, "test")

    answer = UserAnswer.objects.get(ticket=ticket, question=question.question)

    assert UserAnswer.objects.count() == 1

    assert response["data"]["sendQuestionAnswer"]["__typename"] == "UserAnswer"
    assert response["data"]["sendQuestionAnswer"]["answer"] == "test"

    assert answer.answer == "test"

    response = _submit_answer(graphql_client, ticket, question.question, "new response")

    answer.refresh_from_db()

    assert UserAnswer.objects.count() == 1

    assert response["data"]["sendQuestionAnswer"]["__typename"] == "UserAnswer"
    assert response["data"]["sendQuestionAnswer"]["answer"] == "new response"

    assert answer.answer == "new response"


@mark.django_db
def test_answer_choice_question(
    graphql_client, user, ticket_factory, ticket_fare_question_factory
):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)
    question = ticket_fare_question_factory(
        ticket_fare=ticket.ticket_fare,
        question__choices=("a", "b", "c"),
        question__question_type="choice",
    )

    response = _submit_answer(graphql_client, ticket, question.question, "a")

    assert response["data"]["sendQuestionAnswer"]["__typename"] == "UserAnswer"
    assert response["data"]["sendQuestionAnswer"]["answer"] == "a"


@mark.django_db
def test_answer_choice_question_with_a_not_allowed_answer(
    graphql_client, user, ticket_factory, ticket_fare_question_factory
):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)
    question = ticket_fare_question_factory(
        ticket_fare=ticket.ticket_fare,
        question__choices=("a", "b", "c"),
        question__question_type="choice",
    )

    response = _submit_answer(graphql_client, ticket, question.question, "test")

    assert (
        response["data"]["sendQuestionAnswer"]["__typename"]
        == "SendQuestionAnswerErrors"
    )
    assert response["data"]["sendQuestionAnswer"]["validationAnswer"] == [
        "Answer not possible for this question."
    ]


@mark.django_db
def test_required_answer_cannot_be_empty(
    graphql_client, user, ticket_factory, ticket_fare_question_factory
):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)
    question = ticket_fare_question_factory(
        ticket_fare=ticket.ticket_fare, question__question_type="text", is_required=True
    )

    response = _submit_answer(graphql_client, ticket, question.question, "")

    assert (
        response["data"]["sendQuestionAnswer"]["__typename"]
        == "SendQuestionAnswerErrors"
    )
    assert response["data"]["sendQuestionAnswer"]["validationAnswer"] == [
        "This question cannot be left blank"
    ]


@mark.django_db
def test_not_required_answer_can_be_empty(
    graphql_client, user, ticket_factory, ticket_fare_question_factory
):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)
    question = ticket_fare_question_factory(
        ticket_fare=ticket.ticket_fare,
        question__question_type="text",
        is_required=False,
    )

    response = _submit_answer(graphql_client, ticket, question.question, "")

    assert response["data"]["sendQuestionAnswer"]["__typename"] == "UserAnswer"
    assert response["data"]["sendQuestionAnswer"]["answer"] == ""


@mark.django_db
def test_cannot_answer_question_on_tickets_of_other_users(
    graphql_client, user, ticket_factory, ticket_fare_question_factory
):
    graphql_client.force_login(user)

    another_user_ticket = ticket_factory()
    question = ticket_fare_question_factory(
        ticket_fare=another_user_ticket.ticket_fare, question__question_type="text"
    )

    response = _submit_answer(
        graphql_client, another_user_ticket, question.question, "test"
    )

    assert (
        response["data"]["sendQuestionAnswer"]["__typename"]
        == "SendQuestionAnswerErrors"
    )
    assert response["data"]["sendQuestionAnswer"]["validationTicket"] == [
        "Select a valid choice. That choice is not one of the available choices."
    ]


@mark.django_db
def test_cannot_answer_question_not_allowed_in_the_ticket_fare(
    graphql_client,
    user,
    ticket_factory,
    ticket_fare_question_factory,
    ticket_question_factory,
):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)
    question = ticket_question_factory()

    response = _submit_answer(graphql_client, ticket, question, "test")

    assert (
        response["data"]["sendQuestionAnswer"]["__typename"]
        == "SendQuestionAnswerErrors"
    )
    assert response["data"]["sendQuestionAnswer"]["validationQuestion"] == [
        "Question not allowed"
    ]
