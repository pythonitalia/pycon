from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import List

import strawberry
from strawberry import LazyType


@strawberry.enum
class VoteValues(Enum):
    NOT_INTERESTED = 0
    MAYBE = 1
    WANT_TO_SEE = 2
    MUST_SEE = 3

    @classmethod
    def from_int(cls, value: int):
        for _, member in cls.__members__.items():
            if member.value == value:
                return member

        return None


@strawberry.type
class VoteType:
    id: strawberry.ID
    value: int
    submission: LazyType["Submission", "api.submissions.types"]


@strawberry.type
class RankRequest:
    is_public: bool
    ranked_submissions: List[RankSubmission]


@strawberry.type
class RankSubmission:
    submission: LazyType["Submission", "api.submissions.types"]
    absolute_rank: int
    absolute_score: Decimal
    topic_rank: int
