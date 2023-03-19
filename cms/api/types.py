from typing import Self
import strawberry

from decimal import Decimal
from page.models import GenericPage as GenericPageModel


@strawberry.type
class TextSection:
    title: str
    subtitle: str
    body: str
    illustration: str

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            title=block.value["title"],
            subtitle=block.value["subtitle"],
            body=block.value["body"],
            illustration=block.value["illustration"],
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
    (TextSection, CMSMap),
)


@strawberry.type
class GenericPage:
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

        return cls(body=blocks)
