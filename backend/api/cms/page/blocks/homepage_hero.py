from enum import Enum
from typing import Self
from api.cms.base.blocks.cta import CTA
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
    title: str
    location: str
    dates: str
    subtitle: str
    highlight: str
    primary_cta: CTA | None
    secondary_cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        city = block.value.get("city")
        primary_cta = block.value.get("primary_cta")
        secondary_cta = block.value.get("secondary_cta")

        return cls(
            id=block.id,
            city=HomepageHeroCity(city) if city else None,
            title=block.value.get("title") or "",
            location=block.value.get("location") or "",
            dates=block.value.get("dates") or "",
            subtitle=block.value.get("subtitle") or "",
            highlight=block.value.get("highlight") or "",
            primary_cta=(
                CTA.from_block(primary_cta)
                if primary_cta and primary_cta["label"]
                else None
            ),
            secondary_cta=(
                CTA.from_block(secondary_cta)
                if secondary_cta and secondary_cta["label"]
                else None
            ),
        )
