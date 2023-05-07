import strawberry
from typing import Optional, Union

from api.permissions import IsAuthenticated


@strawberry.input
class ScanBadgeInput:
    url: str


@strawberry.type
class Attendee:
    full_name: str
    email: str


@strawberry.type
class BadgeScan:
    attendee: Attendee
    notes: Optional[str]


@strawberry.type
class ScanSuccess:
    badge_scan: BadgeScan


@strawberry.type
class ScanError:
    message: str


@strawberry.type
class BadgeScannerMutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
    )
    def scan_badge(self, input: ScanBadgeInput) -> Union[ScanSuccess, ScanError]:
        pass
