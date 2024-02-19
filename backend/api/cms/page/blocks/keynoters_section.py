from typing import Self
from api.cms.page.registry import register_page_block
import strawberry

from api.cms.base.blocks.cta import CTA


@register_page_block
@strawberry.type
class KeynotersSection:
    id: strawberry.ID
    title: str
    cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        cta = block.value["cta"]
        return cls(
            id=block.id,
            title=block.value["title"],
            cta=CTA.from_block(cta) if cta["label"] else None,
        )
