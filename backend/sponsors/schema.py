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
        sponsors = Sponsor.objects.filter(level__conference__code=code).select_related(
            "level"
        )

        by_level = groupby(sponsors, key=lambda sponsor: sponsor.level.name)

        return [SponsorsByLevel(level, list(sponsors)) for level, sponsors in by_level]
