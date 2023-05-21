from __future__ import annotations
from api.helpers.ids import decode_hashid
from django.core.files.base import ContentFile

import pretix
import re
import strawberry
from api.context import Info

from api.permissions import IsAuthenticated
from badge_scanner import models
from conferences.models import Conference
from users.client import get_user_by_email

from .types import BadgeScan, BadgeScanExport


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


@strawberry.input
class UpdateBadgeScanInput:
    id: str
    notes: str


@strawberry.type
class BadgeScannerMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def scan_badge(self, info: Info, input: ScanBadgeInput) -> BadgeScan | ScanError:
        conference = Conference.objects.filter(code=input.conference_code).first()

        if not conference:
            return ScanError(message="Conference not found")

        if error := input.validate():
            return error

        order_position_data = pretix.get_order_position(
            conference, input.order_position_id
        )

        user = get_user_by_email(order_position_data["attendee_email"])

        scanned_badge, _ = models.BadgeScan.objects.get_or_create(
            scanned_by_id=info.context.request.user.id,
            scanned_user_id=user["id"] if user else None,
            badge_url=input.url,
            conference=conference,
            attendee_name=order_position_data["attendee_name"],
            attendee_email=order_position_data["attendee_email"],
            defaults={
                "notes": "",
            },
        )

        return BadgeScan.from_db(scanned_badge)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_badge_scan(
        self, info: Info, input: UpdateBadgeScanInput
    ) -> BadgeScan | ScanError:
        badge_scan = models.BadgeScan.objects.filter(
            scanned_by_id=info.context.request.user.id, id=input.id
        ).first()

        if not badge_scan:
            return ScanError(message="Badge scan not found")

        badge_scan.notes = input.notes
        badge_scan.save()

        return BadgeScan.from_db(badge_scan)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def export_badge_scans(self, info: Info, conference_code: str) -> BadgeScanExport:
        conference = Conference.objects.filter(code=conference_code).first()

        if conference is None:
            raise ValueError("Unable to find conference")

        current_user_scans = models.BadgeScan.objects.filter(
            scanned_by_id=info.context.request.user.id, conference__code=conference_code
        )

        import tablib

        data = tablib.Dataset(
            headers=["Created", "Attendee Name", "Attendee Email", "Notes"]
        )

        for scan in current_user_scans:
            data.append(
                [scan.created, scan.attendee_name, scan.attendee_email, scan.notes]
            )

        csv_data = data.export("csv").encode("utf-8")

        badge_scan_export = models.BadgeScanExport.objects.create(
            conference_id=conference.id,
            requested_by_id=info.context.request.user.id,
            file=ContentFile(csv_data, name="badge_scans.csv"),
        )

        return BadgeScanExport.from_db(badge_scan_export)
