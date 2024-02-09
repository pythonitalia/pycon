from django_admin_api.schedule.types.room import Room
from django_admin_api.schedule.types.user import User
from django_admin_api.schedule.types.submission import Submission
import strawberry


@strawberry.type
class ScheduleItem:
    id: strawberry.ID
    type: str
    title: str
    status: str
    duration: int | None
    submission: Submission | None
    rooms: list[Room]
    speakers: list[User]

    @classmethod
    def from_model(cls, item):
        return cls(
            id=item.id,
            type=item.type,
            title=item.title,
            status=item.status,
            duration=item.duration,
            rooms=[Room.from_model(room) for room in item.rooms.all()],
            submission=Submission.from_model(item.submission)
            if item.submission_id
            else None,
            speakers=[User.from_model(speaker) for speaker in item.speakers],
        )
