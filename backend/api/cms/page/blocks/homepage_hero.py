from enum import Enum
from typing import Self
from api.cms.page.registry import register_page_block
import strawberry


@strawberry.enum
class HomepageHeroCity(Enum):
    FLORENCE = "florence"
    BOLOGNA = "bologna"


@register_page_block
@strawberry.type
class HomepageHero:
    id: strawberry.ID
    city: HomepageHeroCity | None

    @classmethod
    def from_block(cls, block) -> Self:
        city = block.value.get("city")
        return cls(
            id=block.id,
            city=HomepageHeroCity(city) if city else None,
        )
