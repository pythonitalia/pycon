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
    pretitle: str
    title: str
    subtitle: str
    highlight: str
    illustration: str
    primary_cta: CTA | None
    secondary_cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        # Blocks saved before a field was added don't have a value for it,
        # Wagtail fills those with the block default, which is None.
        city = block.value["city"]
        primary_cta = block.value["primary_cta"]
        secondary_cta = block.value["secondary_cta"]

        return cls(
            id=block.id,
            city=HomepageHeroCity(city) if city else None,
            pretitle=block.value["pretitle"] or "",
            title=block.value["title"] or "",
            subtitle=block.value["subtitle"] or "",
            highlight=block.value["highlight"] or "",
            illustration=block.value["illustration"] or "",
            primary_cta=(CTA.from_block(primary_cta) if primary_cta["label"] else None),
            secondary_cta=(
                CTA.from_block(secondary_cta) if secondary_cta["label"] else None
            ),
        )
