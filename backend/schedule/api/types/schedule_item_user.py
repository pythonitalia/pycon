import strawberry
import strawberry_django

from participants.api.types import Participant
from users import models as user_models


@strawberry.type
class ScheduleItemUser:
    id: strawberry.ID
    fullname: str
    full_name: str
    _user: strawberry.Private[user_models.User]
    _conference_id: strawberry.Private[int]

    @strawberry_django.field
    def participant(self) -> Participant | None:
        return next(
            (
                participant
                for participant in self._user.participants.all()
                if participant.conference_id == self._conference_id
            ),
            None,
        )
