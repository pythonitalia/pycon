from __future__ import annotations

import strawberry
from api.context import Info
from api.permissions import IsAuthenticated
from badge_scanner import models


from api.types import Paginated, PageInfo
from .types import BadgeScan


@strawberry.type
class BadgeScannerQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def badge_scans(
        self, info: Info, conference_code: str, page: int | None = 1
    ) -> Paginated[BadgeScan]:
        scans = models.BadgeScan.objects.filter(
            conference__code=conference_code,
            scanned_by_id=info.context.request.user.id,
        ).order_by("-created")

        page = page or 1
        total_scans = scans.count()
        page_size = 100

        return Paginated.paginate_list(
            items=[BadgeScan.from_db(scan) for scan in scans],
            page_size=page_size,
            total_items=total_scans,
            page=page,
        )
