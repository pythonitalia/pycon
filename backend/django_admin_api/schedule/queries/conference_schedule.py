from conferences.models.conference import Conference
from django_admin_api.schedule.types.day import Day
import strawberry


@strawberry.type
class Schedule:
    id: strawberry.ID
    days: list[Day]

    @classmethod
    def from_model(cls, conference: Conference) -> "Schedule":
        return cls(
            id=conference.id,
            days=[Day.from_model(day) for day in conference.days.all()],
        )


@strawberry.field
def conference_schedule(conference_id: strawberry.ID) -> Schedule:
    conference = Conference.objects.prefetch_related(
        "days",
        "days__slots",
        "days__added_rooms",
        "days__slots__items",
        "days__slots__items__rooms",
        "days__slots__items__keynote",
        "days__slots__items__submission",
        "days__slots__items__submission__speaker",
        "days__slots__items__additional_speakers",
        "days__slots__items__keynote__speakers__user",
    ).get(id=conference_id)
    return Schedule.from_model(conference)
