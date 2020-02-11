from typing import TYPE_CHECKING, List, Optional

import strawberry
from api.submissions.types import Submission
from api.users.types import User
from strawberry.types.datetime import DateTime

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import Conference


@strawberry.type
class Room:
    id: strawberry.ID
    name: str
    conference: "Conference"
    type: str


@strawberry.type
class ScheduleItem:
    id: strawberry.ID
    conference: "Conference"
    start: DateTime
    end: DateTime
    submission: Optional[Submission]
    slug: str
    description: str
    type: str
    highlight_color: Optional[str]
    speakers: List[User]

    @strawberry.field
    def title(self, info) -> str:
        return self.submission.title if self.submission else self.title

    @strawberry.field
    def rooms(self, info) -> List[Room]:
        return self.rooms.all()

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context["request"].build_absolute_uri(self.image.url)
