from enum import Enum
from typing import List, Optional

import strawberry
from conferences.types import TicketFare
from users.types import User

from . import QUESTION_TYPE_CHOICE, QUESTION_TYPE_TEXT


@strawberry.enum
class QuestionType(Enum):
    TEXT = QUESTION_TYPE_TEXT
    CHOICE = QUESTION_TYPE_CHOICE


@strawberry.type
class TicketQuestionChoice:
    choice: str


@strawberry.type
class TicketQuestion:
    text: str
    question_type: QuestionType

    @strawberry.field
    def choices(self, info) -> List[TicketQuestionChoice]:
        return self.choices.all()


@strawberry.type
class UserAnswer:
    question: TicketQuestion
    answer: Optional[str]


@strawberry.type
class Ticket:
    id: strawberry.ID
    user: User
    ticket_fare: TicketFare

    @strawberry.field
    def answers(self, info) -> List[UserAnswer]:
        # TODO: Replace with a JOIN or something else,
        # to make everything run in a single query
        fare_questions = self.ticket_fare.questions.select_related("question").all()
        answers = list(self.answers.all())

        response = []

        for fare_question in fare_questions:
            found_answer = [
                answer.answer
                for answer in answers
                if answer.question_id == fare_question.question.id
            ]
            found_answer = found_answer[0] if found_answer else None

            response.append(
                UserAnswer(question=fare_question.question, answer=found_answer)
            )

        return response
