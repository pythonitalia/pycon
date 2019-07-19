from datetime import datetime
from typing import List

import pytz
import strawberry
from api.scalars import Date, DateTime
from languages.types import LanguageType
from schedule.types import RoomType, ScheduleItemType
from submissions.types import SubmissionType, SubmissionTypeType


@strawberry.type
class AudienceLevelType:
    id: strawberry.ID
    name: str


@strawberry.type
class TopicType:
    id: strawberry.ID
    name: str


@strawberry.type
class ConferenceType:
    id: strawberry.ID

    name: str
    code: str
    start: DateTime
    end: DateTime

    @strawberry.field
    def timezone(self, info) -> str:
        return str(self.timezone)

    @strawberry.field
    def schedule(self, info, date: Date = None) -> List[ScheduleItemType]:
        qs = self.schedule_items

        if date:
            start_date = datetime.combine(date, datetime.min.time())
            end_date = datetime.combine(date, datetime.max.time())

            utc_start_date = pytz.utc.normalize(start_date.astimezone(pytz.utc))
            utc_end_date = pytz.utc.normalize(end_date.astimezone(pytz.utc))

            qs = qs.filter(start__gte=utc_start_date, end__lte=utc_end_date)

        return qs.order_by("start")

    @strawberry.field
    def ticket_fares(self, info) -> List["TicketFareType"]:
        return self.ticket_fares.all()

    @strawberry.field
    def deadlines(self, info) -> List["DeadlineType"]:
        return self.deadlines.order_by("start").all()

    @strawberry.field
    def audience_levels(self, info) -> List[AudienceLevelType]:
        return self.audience_levels.all()

    @strawberry.field
    def topics(self, info) -> List[TopicType]:
        return self.topics.all()

    @strawberry.field
    def languages(self, info) -> List[LanguageType]:
        return self.languages.all()

    @strawberry.field
    def durations(self, info) -> List["DurationType"]:
        return self.durations.all()

    @strawberry.field
    def submissions(self, info) -> List[SubmissionType]:
        return self.submissions.all()

    @strawberry.field
    def rooms(self, info) -> List[RoomType]:
        return self.rooms.all()


@strawberry.type
class DeadlineType:
    type: str
    name: str
    start: DateTime
    end: DateTime
    conference: ConferenceType


@strawberry.type
class TicketFareType:
    id: strawberry.ID
    code: str
    name: str
    price: str
    start: DateTime
    end: DateTime
    description: str
    conference: ConferenceType


@strawberry.type
class DurationType:
    id: strawberry.ID
    conference: ConferenceType
    name: str
    duration: int
    notes: str

    @strawberry.field
    def allowed_submission_types(self, info) -> List[SubmissionTypeType]:
        return self.allowed_submission_types.all()
