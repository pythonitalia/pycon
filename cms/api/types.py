from typing import Self
import strawberry

from decimal import Decimal
from page.models import GenericPage as GenericPageModel


@strawberry.type
class TextSection:
    id: strawberry.ID
    title: str
    subtitle: str
    body: str
    illustration: str

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            title=block.value["title"],
            subtitle=block.value["subtitle"],
            body=block.value["body"],
            illustration=block.value["illustration"],
        )

@strawberry.type
class Accordion:
    title: str
    body: str
    is_open: bool

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            title=block["title"],
            body=block["body"],
            is_open=block["is_open"],
        )

@strawberry.type
class TextSectionWithAccordion(TextSection):
    accordions: list[Accordion]

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            title=block.value["title"],
            subtitle=block.value["subtitle"],
            body=block.value["body"],
            illustration=block.value["illustration"],
            accordions=[Accordion.from_block(accordion)
                        for accordion in block.value["accordions"]]
        )

@strawberry.type
class CMSMap:
    latitude: Decimal
    longitude: Decimal

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            latitude=block.value["latitude"],
            longitude=block.value["longitude"],
        )


Block = strawberry.union(
    "Block",
    (TextSection, TextSectionWithAccordion, CMSMap),
)


@strawberry.type
class GenericPage:
    id: strawberry.ID
    body: list[Block]

    @classmethod
    def from_model(cls, obj: GenericPageModel) -> Self:
        blocks = []

        for block in obj.body:
            match block.block_type:
                case "text_section":
                    blocks.append(TextSection.from_block(block))
                case "text_section_with_accordion":
                    blocks.append(TextSectionWithAccordion.from_block(block))
                case "map":
                    blocks.append(CMSMap.from_block(block))

        return cls(id=obj.id, body=blocks)
