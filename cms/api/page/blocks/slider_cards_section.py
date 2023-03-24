from typing import Self
import strawberry

from api.base.blocks.cta import CTA


@strawberry.type
class SimpleTextCard:
    title: str
    body: str
    cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            title=block["title"],
            body=block["body"],
            cta=CTA.from_block(cta) if (cta := block["cta"]) else None,
        )


@strawberry.type
class SliderCardsSection:
    id: strawberry.ID
    cards: list[SimpleTextCard]

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            cards=[SimpleTextCard.from_block(card) for card in block.value["cards"]],
        )
