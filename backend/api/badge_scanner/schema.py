from __future__ import annotations

import pretix
import re
from typing import Any
import strawberry
from strawberry.types.info import Info

from api.permissions import IsAuthenticated
from badge_scanner import models
from conferences.models import Conference
from users.client import get_user_by_email


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
    notes: str


@strawberry.type
class BadgeScannerMutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
    )
    def scan_badge(
        self, info: Info[Any, None], input: ScanBadgeInput
    ) -> BadgeScan | ScanError:
        conference = Conference.objects.filter(code=input.conference_code).first()

        if not conference:
            return ScanError(message="Conference not found")

        if error := input.validate():
            return error

        data = pretix.get_order_position(conference, input.order_position_id)

        user = get_user_by_email(data["attendee_email"])

        if user is None:
            return ScanError(message="User not found")

        scanned_badge, _ = models.BadgeScan.objects.get_or_create(
            scanned_by_id=info.context.request.user.id,
            scanned_user_id=user["id"],
            badge_url=input.url,
            conference=conference,
            defaults={
                "notes": "",
            },
        )

        return BadgeScan(
            attendee=Attendee(
                full_name=data["attendee_name"], email=data["attendee_email"]
            ),
            notes=scanned_badge.notes,
        )
