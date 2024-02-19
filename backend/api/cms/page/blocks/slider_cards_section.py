from typing import Annotated, Self
import strawberry

from api.cms.base.blocks.cta import CTA
from api.cms.base.types import Spacing


@strawberry.type
class SimpleTextCard:
    title: str
    body: str
    cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        cta = block.value["cta"]
        return cls(
            title=block.value["title"],
            body=block.value["body"],
            cta=CTA.from_block(cta) if cta["label"] else None,
        )


@strawberry.type
class PriceCard:
    title: str
    body: str
    price: str
    price_tier: str
    cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        cta = block.value["cta"]
        return cls(
            title=block.value["title"],
            body=block.value["body"],
            price=block.value["price"],
            price_tier=block.value["price_tier"],
            cta=CTA.from_block(cta) if cta["label"] else None,
        )


AvailableCards = Annotated[
    SimpleTextCard | PriceCard, strawberry.union("AvailableCards")
]


@strawberry.type
class SliderCardsSection:
    id: strawberry.ID
    title: str
    spacing: Spacing
    snake_background: bool
    cards: list[AvailableCards]

    @classmethod
    def from_block(cls, block) -> Self:
        cards = []
        for card in block.value["cards"]:
            match card.block_type:
                case "simple_text_card":
                    cards.append(SimpleTextCard.from_block(card))
                case "price_card":
                    cards.append(PriceCard.from_block(card))

        return cls(
            id=block.id,
            title=block.value["title"],
            snake_background=block.value["snake_background"],
            spacing=Spacing(block.value["spacing"]),
            cards=cards,
        )
