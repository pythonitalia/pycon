from api.participants.types import Participant
import strawberry


@strawberry.type
class ScheduleItemUser:
    id: strawberry.ID
    fullname: str
    full_name: str
    participant: Participant | None
