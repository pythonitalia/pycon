from typing import List, Optional

import strawberry
from api.scalars import DateTime
from submissions.types import Submission
from users.types import UserType

if False:
    from conferences.types import Conference


@strawberry.type
class Room:
    name: str
    conference: "Conference"


@strawberry.type
class ScheduleItem:
    id: strawberry.ID
    conference: "Conference"
    start: DateTime
    end: DateTime
    submission: Optional[Submission]
    title: str
    description: str
    type: str

    @strawberry.field
    def additional_speakers(self, info) -> List[UserType]:
        return self.additional_speakers.all()

    @strawberry.field
    def rooms(self, info) -> List[Room]:
        return self.rooms.all()
