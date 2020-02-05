import typing
from datetime import date, datetime, time, timedelta

import strawberry
from api.conferences.types import Day, ScheduleSlot
from conferences.models import Conference
from schedule.models import Day as DayModel
from strawberry.types.datetime import Date


@strawberry.type
class AddScheduleSlotError:
    message: str


def add_minutes_to_time(time: time, minutes: int) -> time:
    return (datetime.combine(date(1, 1, 1), time) + timedelta(minutes=minutes)).time()


# TODO: permission
@strawberry.type
class ScheduleMutations:
    @strawberry.mutation
    def add_schedule_slot(
        self, info, conference: strawberry.ID, duration: int, day: Date
    ) -> typing.Union[AddScheduleSlotError, Day]:
        conference = Conference.objects.get(code=conference)
        day, _ = DayModel.objects.get_or_create(day=day, conference=conference)

        schedule_configuration = day.schedule_configuration

        # TODO: is it ok to hardcode this?
        hour = "08:45"
        offset = 0

        if len(schedule_configuration):
            last_slot = schedule_configuration[-1]

            hour = time.strftime(
                add_minutes_to_time(
                    time.fromisoformat(last_slot["hour"]), last_slot["duration"]
                ),
                "%H:%M",
            )

            offset = last_slot["offset"] + last_slot["size"]

        schedule_configuration.append(
            {"hour": hour, "offset": offset, "duration": duration, "size": 45}
        )

        day.schedule_configuration = schedule_configuration
        day.save()

        return Day(
            day=day.day,
            schedule_configuration=[
                ScheduleSlot(**info) for info in schedule_configuration
            ],
        )
