from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import List

import strawberry

from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from api.submissions.types import Submission


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
    submission: Annotated["Submission", strawberry.lazy("api.submissions.types")]


@strawberry.type
class RankStat:
    id: strawberry.ID
    type: str
    name: str
    value: int


@strawberry.type
class RankRequest:
    is_public: bool
    ranked_submissions: List[RankSubmission]
    stats: List[RankStat]


@strawberry.type
class RankSubmission:
    submission: Annotated["Submission", strawberry.lazy("api.submissions.types")]
    rank: int
    score: Decimal
