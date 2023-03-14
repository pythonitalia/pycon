from __future__ import annotations
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
    def from_block(cls, block) -> TextSection:
        return cls(
            title=block.value["title"],
            subtitle=block.value["subtitle"],
            body=block.value["body"],
            illustration=block.value["illustration"],
        )


@strawberry.type
class Map:
    latitude: Decimal
    longitude: Decimal

    @classmethod
    def from_block(cls, block) -> Map:
        return cls(
            latitude=block.value["latitude"],
            longitude=block.value["longitude"],
        )


@strawberry.type
class Image:
    title: str
    width: int
    height: int
    url: str

    @classmethod
    def from_block(cls, block) -> Image:
        return cls(
            title=block.value.title,
            width=block.value.width,
            height=block.value.height,
            url=block.value.file.url,
        )


Block = strawberry.union(
    "Block",
    (TextSection, Map, Image),
)


@strawberry.type
class GenericPage:
    body: list[Block]

    @classmethod
    def from_model(cls, obj: GenericPageModel) -> GenericPage:
        blocks = []

        for block in obj.body:
            match block.block_type:
                case "text_section":
                    blocks.append(TextSection.from_block(block))
                case "map":
                    blocks.append(Map.from_block(block))
                case "image":
                    blocks.append(Image.from_block(block))

        return cls(body=blocks)
