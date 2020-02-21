import dataclasses
import typing

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


def convert_user_to_endpoint(user: User) -> Endpoint:
    has_sent_submission_to = Submission.objects.filter(speaker=user).values_list(
        "conference__code", flat=True
    )
    has_item_in_schedule = ScheduleItem.objects.filter(
        Q(submission__speaker=user) | Q(additional_speakers=user)
    ).values_list("conference__code", flat=True)

    return Endpoint(
        id=str(user.id),
        name=user.name,
        full_name=user.full_name,
        email=user.email,
        is_staff=user.is_staff,
        has_sent_submission_to=list(has_sent_submission_to),
        has_item_in_schedule=list(has_item_in_schedule),
        has_cancelled_talks=[],
    )
