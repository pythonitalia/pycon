from enum import Enum
from typing import List

import strawberry
from conferences.types import TicketFare
from users.types import UserType

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
    answer: str


@strawberry.type
class TicketType:
    id: strawberry.ID
    user: UserType
    ticket_fare: TicketFare

    # @strawberry.field
    # def answers(self, info) -> List[UserAnswer]:
    #     return self.answers.all()
