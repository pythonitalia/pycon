from __future__ import annotations

import pretix
import re
import strawberry
from typing import Optional, Union

from api.permissions import IsAuthenticated
from conferences.models import Conference


@strawberry.type
class ScanError:
    message: str


@strawberry.input
class ScanBadgeInput:
    url: str
    conference_code: str

    url_regex = re.compile(r"^https://pycon\.it/b/([\w\d-]+)$")

    def validate(self) -> ScanError | None:
        if not self.url:
            return ScanError(message="URL is required")

        match = self.url_regex.match(self.url)

        return None if match else ScanError(message="URL is not valid")

    @property
    def order_position_id(self) -> str:
        match = self.url_regex.match(self.url)

        assert match

        return match.group(1)


@strawberry.type
class Attendee:
    full_name: str
    email: str


@strawberry.type
class BadgeScan:
    attendee: Attendee
    notes: Optional[str]


@strawberry.type
class BadgeScannerMutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
    )
    def scan_badge(self, input: ScanBadgeInput) -> Union[BadgeScan, ScanError]:
        conference = Conference.objects.filter(code=input.conference_code).first()

        if not conference:
            return ScanError(message="Conference not found")

        if error := input.validate():
            return error

        data = pretix.get_order_position(conference, input.order_position_id)

        return BadgeScan(
            attendee=Attendee(
                full_name=data["attendee_name"], email=data["attendee_email"]
            ),
            notes=None,
        )
