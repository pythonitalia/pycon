from typing import Self
import strawberry

from api.base.blocks.accordion import Accordion
from api.base.blocks.cta import CTA


@strawberry.type
class TextSection:
    id: strawberry.ID
    title: str
    is_main_title: bool
    subtitle: str
    body: str
    illustration: str
    accordions: list[Accordion]
    cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        cta = block.value["cta"]
        return cls(
            id=block.id,
            title=block.value["title"],
            is_main_title=block.value["is_main_title"],
            subtitle=block.value["subtitle"],
            body=block.value["body"],
            illustration=block.value["illustration"],
            accordions=[
                Accordion.from_block(accordion)
                for accordion in block.value["accordions"]
            ],
            cta=CTA.from_block(cta) if cta["label"] else None,
        )
