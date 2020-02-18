from typing import TYPE_CHECKING, List, Optional

import strawberry
from api.languages.types import Language
from api.submissions.types import Submission
from api.users.types import User
from strawberry.types.datetime import DateTime
from users.models import User as UserModel

if TYPE_CHECKING:  # pragma: no cover
    from api.conferences.types import Conference, AudienceLevel  # noqa


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
    title: str
    start: DateTime
    end: DateTime
    submission: Optional[Submission]
    slug: str
    description: str
    type: str
    duration: Optional[int]
    highlight_color: Optional[str]
    speakers: List[User]
    language: Language
    audience_level: Optional["AudienceLevel"]

    @strawberry.field
    def rooms(self, info) -> List[Room]:
        return self.rooms.all()

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context["request"].build_absolute_uri(self.image.url)

    @strawberry.field
    def my_interest(self, info) -> bool:
        request = info.context["request"]
        try:
            self.subscribed_users.get(id=request.user.id)
        except UserModel.DoesNotExist:
            return False
        return True
