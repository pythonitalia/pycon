from __future__ import annotations

import strawberry
from api.permissions import IsAuthenticated


from api.types import Paginated
from .types import BadgeScan


@strawberry.type
class BadgeScannerQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def badge_scans(
        self, conference_code: str, page: int | None = 1
    ) -> Paginated[BadgeScan]:
        pass
