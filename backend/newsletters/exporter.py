import dataclasses
import typing
from collections import defaultdict

from django.db.models import Q
from schedule.models import ScheduleItem
from submissions.models import Submission
from users.models import User


@dataclasses.dataclass(frozen=True)
class Endpoint:
    id: typing.Union[str]
    name: str = dataclasses.field(hash=False)
    email: str = dataclasses.field(hash=False)
    full_name: str = dataclasses.field(hash=False)
    is_staff: bool = dataclasses.field(hash=False)
    has_sent_submission_to: typing.List[str] = dataclasses.field(hash=False)
    has_item_in_schedule: typing.List[str] = dataclasses.field(hash=False)
    has_cancelled_talks: typing.List[str] = dataclasses.field(hash=False)
    talks_by_conference: typing.Dict[str, typing.List[str]] = dataclasses.field(
        hash=False
    )


def convert_user_to_endpoint(user: User) -> Endpoint:
    has_sent_submission_to = Submission.objects.filter(speaker=user).values_list(
        "conference__code", flat=True
    )
    schedule_items = ScheduleItem.objects.filter(
        Q(submission__speaker=user) | Q(additional_speakers=user)
    ).values("conference__code", "title")

    talks_by_conference: typing.DefaultDict[str, typing.List[str]] = defaultdict(list)

    for item in schedule_items:
        talks_by_conference[item["conference__code"]].append(item["title"])

    return Endpoint(
        id=str(user.id),
        name=user.name,
        full_name=user.full_name,
        email=user.email,
        is_staff=user.is_staff,
        has_sent_submission_to=list(has_sent_submission_to),
        has_item_in_schedule=list(talks_by_conference),
        has_cancelled_talks=[],
        talks_by_conference=talks_by_conference,
    )
