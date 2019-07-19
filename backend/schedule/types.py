from typing import List, Optional

import strawberry
from api.scalars import DateTime
from submissions.types import SubmissionType
from users.types import UserType

if False:
    from conferences.types import ConferenceType


@strawberry.type
class RoomType:
    name: str
    conference: "ConferenceType"


@strawberry.type
class ScheduleItemType:
    id: strawberry.ID
    conference: "ConferenceType"
    start: DateTime
    end: DateTime
    submission: Optional[SubmissionType]
    title: str
    description: str
    type: str

    @strawberry.field
    def additional_speakers(self, info) -> List[UserType]:
        return self.additional_speakers.all()

    @strawberry.field
    def rooms(self, info) -> List[RoomType]:
        return self.rooms.all()
