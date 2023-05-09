from __future__ import annotations

import re
import strawberry
from typing import Optional, Union

from api.permissions import IsAuthenticated


@strawberry.type
class ScanError:
    message: str


@strawberry.input
class ScanBadgeInput:
    url: str

    url_regex = re.compile(r"^https://pycon\.it/b/([\w\d-]+)$")

    def validate(self) -> ScanError | None:
        if not self.url:
            return ScanError(message="URL is required")

        match = self.url_regex.match(self.url)

        return None if match else ScanError(message="URL is not valid")


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
        if error := input.validate():
            return error

        # TODO: find attendee by url

        return BadgeScan(
            attendee=Attendee(full_name="Test User", email="some@email.com"),
            notes=None,
        )
