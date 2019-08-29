from itertools import groupby
from typing import List

import strawberry

from .models import Sponsor
from .types import SponsorsByLevel


@strawberry.type
class SponsorsQuery:
    # TODO: use custom scalar for code and update custom gatsby source to use
    # that instead of a generic argument called code

    @strawberry.field
    def sponsors_by_level(self, info, code: str) -> List[SponsorsByLevel]:
        # TODO: level might need an order
        sponsors = Sponsor.objects.filter(conference__code=code).order_by("level")

        by_level = groupby(sponsors, key=lambda sponsor: sponsor.level)

        return [SponsorsByLevel(level, list(sponsors)) for level, sponsors in by_level]
