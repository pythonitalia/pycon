from strawberry import LazyType

from typing import TYPE_CHECKING, List, Optional

import strawberry
from api.languages.types import Language
from api.submissions.types import Submission
from api.users.types import User
from datetime import datetime


if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import Conference, AudienceLevel  # noqa


@strawberry.type
class Room:
    id: strawberry.ID
    name: str
    conference: LazyType["Conference", "api.conferences.types"]
    type: str


@strawberry.type
class ScheduleItem:
    id: strawberry.ID
    conference: LazyType["Conference", "api.conferences.types"]
    title: str
    start: datetime
    end: datetime
    submission: Optional[Submission]
    slug: str
    description: str
    type: str
    duration: Optional[int]
    highlight_color: Optional[str]
    speakers: List[User]
    language: Language
    audience_level: Optional[LazyType["AudienceLevel", "api.conferences.types"]]

    @strawberry.field
    def rooms(self, info) -> List[Room]:
        return self.rooms.all()

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context.request.build_absolute_uri(self.image.url)
