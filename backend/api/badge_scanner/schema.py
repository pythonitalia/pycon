from __future__ import annotations
from api.helpers.ids import decode_hashid

import pretix
import re
from typing import Any
import strawberry
from strawberry.types.info import Info

from api.permissions import IsAuthenticated
from badge_scanner import models
from conferences.models import Conference
from users.client import get_user_by_email, get_users_data_by_ids


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

        return str(decode_hashid(match.group(1)))


@strawberry.type
class Attendee:
    full_name: str
    email: str


@strawberry.type
class BadgeScan:
    notes: str
    attendee_id: strawberry.Private[int]

    @strawberry.field
    def attendee(self) -> Attendee:
        user_data = get_users_data_by_ids([self.attendee_id]).get(str(self.attendee_id))

        assert user_data

        return Attendee(
            full_name=user_data["fullname"],
            email=user_data["email"],
        )

    @classmethod
    def from_db(cls, db_scan: models.BadgeScan) -> BadgeScan:
        return BadgeScan(
            attendee_id=db_scan.scanned_user_id,
            notes=db_scan.notes,
        )


@strawberry.input
class UpdateBadgeScanInput:
    id: str
    notes: str


@strawberry.type
class BadgeScannerMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def scan_badge(
        self, info: Info[Any, None], input: ScanBadgeInput
    ) -> BadgeScan | ScanError:
        conference = Conference.objects.filter(code=input.conference_code).first()

        if not conference:
            return ScanError(message="Conference not found")

        if error := input.validate():
            return error

        order_position_data = pretix.get_order_position(
            conference, input.order_position_id
        )

        user = get_user_by_email(order_position_data["attendee_email"])

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

        return BadgeScan.from_db(scanned_badge)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_badge_scan(
        self, info: Info[Any, None], input: UpdateBadgeScanInput
    ) -> BadgeScan | ScanError:
        badge_scan = models.BadgeScan.objects.filter(
            scanned_by_id=info.context.request.user.id, id=input.id
        ).first()

        if not badge_scan:
            return ScanError(message="Badge scan not found")

        badge_scan.notes = input.notes
        badge_scan.save()

        return BadgeScan.from_db(badge_scan)
