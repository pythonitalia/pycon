import dataclasses

from typing import DefaultDict
from collections import defaultdict

from django.db.models import Q

from conferences.models import Conference
from pretix import user_has_admission_ticket
from schedule.models import ScheduleItem
from submissions.models import Submission
from users.models import User


@dataclasses.dataclass(frozen=True)
class Endpoint:
    id: str
    name: str = dataclasses.field(hash=False)
    email: str = dataclasses.field(hash=False)
    full_name: str = dataclasses.field(hash=False)
    is_staff: bool = dataclasses.field(hash=False)
    has_sent_submission_to: list[str] = dataclasses.field(hash=False)
    has_item_in_schedule: list[str] = dataclasses.field(hash=False)
    has_cancelled_talks: list[str] = dataclasses.field(hash=False)
    has_ticket: list[str] = dataclasses.field(hash=False)
    talks_by_conference: dict[str, list[str]] = dataclasses.field(hash=False)

    def to_item(self):
        conferences_talks = {
            f"{code}_items_in_schedule": items
            for code, items in self.talks_by_conference.items()
        }

        return {
            "ChannelType": "EMAIL",
            "Address": self.email,
            "Id": self.id,
            "User": {
                "UserId": self.id,
                "UserAttributes": {
                    "Name": [self.name],
                    "FullName": [self.full_name],
                    "is_staff": [str(self.is_staff)],
                    "has_item_in_schedule": self.has_item_in_schedule,
                    "has_cancelled_talks": self.has_cancelled_talks,
                    "has_ticket": self.has_ticket,
                    **conferences_talks,
                },
            },
        }


def convert_user_to_endpoint(user: User) -> Endpoint:
    pretix_conferences = Conference.objects.exclude(pretix_event_id__exact="")
    submissions = Submission.objects.filter(speaker_id=user.id).values(
        "conference__code", "status"
    )
    schedule_items = ScheduleItem.objects.filter(
        Q(submission__speaker_id=user.id) | Q(additional_speakers__user_id=user.id)
    ).values("conference__code", "title")

    talks_by_conference: DefaultDict[str, list[str]] = defaultdict(list)

    for item in schedule_items:
        talks_by_conference[item["conference__code"]].append(item["title"])

    return Endpoint(
        id=str(user.id),
        name=user.name,
        full_name=user.full_name,
        email=user.email,
        is_staff=user.is_staff,
        has_sent_submission_to=list(
            set([submission["conference__code"] for submission in submissions])
        ),
        has_item_in_schedule=list(talks_by_conference),
        has_ticket=[
            conference.code
            for conference in pretix_conferences
            if user_has_admission_ticket(
                email=user.email,
                event_organizer=conference.pretix_organizer_id,
                event_slug=conference.pretix_event_id,
            )
        ],
        has_cancelled_talks=list(
            set(
                [
                    submission["conference__code"]
                    for submission in submissions
                    if submission["status"] == Submission.STATUS.cancelled
                ]
            )
        ),
        talks_by_conference=talks_by_conference,
    )
