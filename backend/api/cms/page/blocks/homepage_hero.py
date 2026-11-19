from enum import Enum
from typing import Self
from api.cms.base.blocks.cta import CTA
from api.cms.page.registry import register_page_block
import strawberry


@strawberry.enum
class HomepageHeroCity(Enum):
    FLORENCE = "florence"
    BOLOGNA = "bologna"


@strawberry.enum
class HomepageHeroVariant(Enum):
    ILLUSTRATION_ONLY = "illustration_only"
    OVERLAY = "overlay"


@register_page_block
@strawberry.type
class HomepageHero:
    id: strawberry.ID
    city: HomepageHeroCity | None
    variant: HomepageHeroVariant
    title: str
    subtitle: str
    body: str
    highlight: str
    primary_cta: CTA | None
    secondary_cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        city = block.value.get("city")
        variant = block.value.get("variant")
        primary_cta = block.value.get("primary_cta")
        secondary_cta = block.value.get("secondary_cta")

        return cls(
            id=block.id,
            city=HomepageHeroCity(city) if city else None,
            variant=HomepageHeroVariant(variant or "illustration_only"),
            title=block.value.get("title") or "",
            subtitle=block.value.get("subtitle") or "",
            body=block.value.get("body") or "",
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
