import dataclasses
import typing

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
    return Endpoint(
        id=str(user.id),
        name=user.name,
        full_name=user.full_name,
        email=user.email,
        is_staff=user.is_staff,
        has_sent_submission_to=[],
        has_item_in_schedule=[],
        has_cancelled_talks=[],
    )
