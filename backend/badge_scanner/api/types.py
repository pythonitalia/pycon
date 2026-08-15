from __future__ import annotations

import strawberry
from datetime import datetime

from badge_scanner import models


@strawberry.type
class Attendee:
    full_name: str
    email: str


@strawberry.type
class BadgeScan:
    id: strawberry.ID
    notes: str
    attendee: Attendee
    created: datetime

    @classmethod
    def from_db(cls, db_scan: models.BadgeScan) -> BadgeScan:
        return BadgeScan(
            id=strawberry.ID(str(db_scan.pk)),
            notes=db_scan.notes,
            attendee=Attendee(
                full_name=db_scan.attendee_name, email=db_scan.attendee_email
            ),
            created=db_scan.created,
        )


@strawberry.type
class BadgeScanExport:
    id: strawberry.ID
    url: str

    @classmethod
    def from_db(cls, db_scan_export: models.BadgeScanExport) -> BadgeScanExport:
        return BadgeScanExport(
            id=strawberry.ID(str(db_scan_export.pk)), url=db_scan_export.file.url
        )
