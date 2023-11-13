from typing import Self
import strawberry

from api.cms.base.blocks.cta import CTA


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
