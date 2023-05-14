from __future__ import annotations

import strawberry

from badge_scanner import models
from users.client import get_users_data_by_ids


@strawberry.type
class Attendee:
    full_name: str
    email: str


@strawberry.type
class BadgeScan:
    id: strawberry.ID
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
            id=strawberry.ID(str(db_scan.pk)),
            attendee_id=db_scan.scanned_user_id,
            notes=db_scan.notes,
        )
