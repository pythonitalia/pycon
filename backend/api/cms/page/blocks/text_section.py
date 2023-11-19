from enum import Enum
from typing import Self
import strawberry

from api.cms.base.blocks.accordion import Accordion
from api.cms.base.blocks.cta import CTA


@strawberry.enum
class BodyTextSize(Enum):
    TEXT_1 = "text-1"
    TEXT_2 = "text-2"


@strawberry.type
class TextSection:
    id: strawberry.ID
    title: str
    is_main_title: bool
    subtitle: str
    body: str
    body_text_size: BodyTextSize
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
            body_text_size=BodyTextSize(block.value["body_text_size"]),
            illustration=block.value["illustration"],
            accordions=[
                Accordion.from_block(accordion)
                for accordion in block.value["accordions"]
            ],
            cta=CTA.from_block(cta) if cta["label"] else None,
        )
