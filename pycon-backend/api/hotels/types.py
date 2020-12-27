import strawberry

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class HotelRoom:
    id: str
    name: str = strawberry.field(resolver=make_localized_resolver("name"))
    description: str = strawberry.field(resolver=make_localized_resolver("description"))
    price: str
    is_sold_out: bool
    capacity_left: int
