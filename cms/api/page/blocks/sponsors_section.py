import enum
from typing import Self
import strawberry

from api.base.blocks.cta import CTA


@strawberry.enum
class SponsorsSectionLayout(enum.Enum):
    SIDE_BY_SIDE = "side-by-side"
    VERTICAL = "vertical"


@strawberry.type
class SponsorsSection:
    id: strawberry.ID
    title: str
    body: str
    cta: CTA | None
    layout: SponsorsSectionLayout

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            title=block.value["title"],
            body=block.value["body"],
            cta=CTA.from_block(block.value["cta"]),
            layout=SponsorsSectionLayout(block.value["layout"]),
        )
