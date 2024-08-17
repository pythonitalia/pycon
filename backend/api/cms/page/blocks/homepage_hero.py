from enum import Enum
from typing import Self
from api.cms.page.registry import register_page_block
import strawberry


@strawberry.enum
class City(Enum):
    FLORENCE = "florence"
    BOLOGNA = "bologna"


@register_page_block
@strawberry.type
class HomepageHero:
    id: strawberry.ID
    city: City | None

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            city=City(block.value["city"]) if block.value["city"] else None,
        )
