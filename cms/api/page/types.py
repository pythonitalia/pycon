from typing import Self
from page.models import GenericPage as GenericPageModel

import strawberry

from api.page.blocks.slider_cards_section import SliderCardsSection
from api.page.blocks.text_section import TextSection
from api.base.blocks.map import CMSMap

Block = strawberry.union(
    "Block",
    (TextSection, CMSMap, SliderCardsSection),
)


@strawberry.type
class GenericPage:
    id: strawberry.ID
    title: str
    body: list[Block]

    @classmethod
    def from_model(cls, obj: GenericPageModel) -> Self:
        blocks = []

        for block in obj.body:
            match block.block_type:
                case "text_section":
                    blocks.append(TextSection.from_block(block))
                case "map":
                    blocks.append(CMSMap.from_block(block))
                case "slider_cards_section":
                    blocks.append(SliderCardsSection.from_block(block))

        return cls(id=obj.id, title=obj.title, body=blocks)
