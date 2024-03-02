from enum import Enum
from typing import Self
from api.cms.page.registry import register_page_block
import strawberry


class CheckoutCategory(Enum):
    TICKETS = "tickets"
    SOCIAL_EVENTS = "social_events"
    TOURS = "tours"
    GADGETS = "gadgets"
    MEMBERSHIP = "membership"
    HOTEL = "hotel"


CheckoutCategoryEnum = strawberry.enum(CheckoutCategory, name="CheckoutCategory")


@register_page_block
@strawberry.type
class CheckoutSection:
    id: strawberry.ID
    visible_categories: list[CheckoutCategoryEnum]

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(id=block.id, visible_categories=cls._get_visible_categories(block))

    @staticmethod
    def _get_visible_categories(block) -> list[CheckoutCategory]:
        categories = []

        match block.value:
            case {"show_conference_tickets_products": True}:
                categories.append(CheckoutCategory.TICKETS)
            case {"show_social_events_products": True}:
                categories.append(CheckoutCategory.SOCIAL_EVENTS)
            case {"show_tours_products": True}:
                categories.append(CheckoutCategory.TOURS)
            case {"show_gadgets_products": True}:
                categories.append(CheckoutCategory.GADGETS)
            case {"show_membership_products": True}:
                categories.append(CheckoutCategory.MEMBERSHIP)
            case {"show_hotel_products": True}:
                categories.append(CheckoutCategory.HOTEL)

        return categories
