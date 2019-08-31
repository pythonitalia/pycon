from pytest import mark


@mark.django_db
def test_get_ticket_answers(
    graphql_client,
    user,
    ticket_factory,
    ticket_fare_question_factory,
    user_answer_factory,
):
    graphql_client.force_login(user)

    ticket = ticket_factory(user=user)

    question1 = ticket_fare_question_factory(
        ticket_fare=ticket.ticket_fare, question__question_type="text"
    )

    question2 = ticket_fare_question_factory(
        ticket_fare=ticket.ticket_fare, question__question_type="text"
    )

    user_answer_factory(ticket=ticket, question=question1.question, answer="hello")

    response = graphql_client.query(
        """
    query($conference: String!) {
        me {
            tickets(conference: $conference) {
                answers {
                    question {
                        text
                    }
                    answer
                }
            }
        }
    }
    """,
        variables={"conference": ticket.ticket_fare.conference.code},
    )

    assert {
        "question": {"text": question1.question.text},
        "answer": "hello",
    } in response["data"]["me"]["tickets"][0]["answers"]

    assert {"question": {"text": question2.question.text}, "answer": None} in response[
        "data"
    ]["me"]["tickets"][0]["answers"]
