from typing import Self
from django.conf import settings
import strawberry

from decimal import Decimal
from page.models import GenericPage as GenericPageModel


@strawberry.type
class CTA:
    label: str
    link: str

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(label=block["label"], link=block["link"])


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


def generate_map_image(
    latitude: Decimal, longitude: Decimal, width: int, height: int, zoom: int
) -> str:
    base = "https://api.mapbox.com/styles/v1/"
    style = "mapbox/streets-v12"
    token = f"access_token={settings.MAPBOX_PUBLIC_API_KEY}"

    coordinates = f"{longitude},{latitude}"
    size = f"{width}x{height}@2x"
    marker = f"pin-s-heart+285A98({coordinates})"

    return f"{base}{style}/static/{marker}/{coordinates},{zoom},0,13/{size}?{token}"


@strawberry.type
class CMSMap:
    id: strawberry.ID
    latitude: Decimal
    longitude: Decimal
    link: str
    zoom: int

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            latitude=block.value["latitude"],
            longitude=block.value["longitude"],
            link=block.value["link"],
            zoom=block.value["zoom"],
        )

    @strawberry.field
    def image(
        self,
        info,
        width: int = 1280,
        height: int = 400,
    ) -> str:
        return generate_map_image(
            latitude=self.latitude,
            longitude=self.longitude,
            width=width,
            height=height,
            zoom=self.zoom,
        )


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


Block = strawberry.union(
    "Block",
    (TextSection, CMSMap, SliderCardsSection),
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
                case "map":
                    blocks.append(CMSMap.from_block(block))
                case "slider_cards_section":
                    blocks.append(SliderCardsSection.from_block(block))

        return cls(id=obj.id, body=blocks)
