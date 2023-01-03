from datetime import timedelta
from typing import List

import strawberry

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class BedLayout:
    id: str
    name: str = strawberry.field(resolver=make_localized_resolver("name"))


@strawberry.type
class HotelRoom:
    id: str
    name: str = strawberry.field(resolver=make_localized_resolver("name"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    price: str
    is_sold_out: bool
    capacity_left: int

    @strawberry.field
    def available_bed_layouts(self) -> List[BedLayout]:
        return self.available_bed_layouts.all()

    @strawberry.field
    def check_in_dates(self) -> List[str]:
        conference_start = self.conference.start
        conference_end = self.conference.end

        nights = (conference_end - conference_start).days
        return [
            (conference_start + timedelta(days=night)).date() for night in range(nights)
        ]

    @strawberry.field
    def check_out_dates(self) -> List[str]:
        conference_start = self.conference.start
        conference_end = self.conference.end

        nights = (conference_end - conference_start).days + 1
        return [
            (conference_start + timedelta(days=night)).date()
            for night in range(1, nights)
        ]
