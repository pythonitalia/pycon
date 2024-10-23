from decimal import Decimal
from typing import Self

import strawberry
from strawberry import ID

from sponsors.models import SponsorLevel as SponsorLevelModel


@strawberry.type
class Sponsor:
    id: ID
    name: str

    @strawberry.field
    def link(self, info) -> str:
        return self.link

    @strawberry.field
    def image(self, info) -> str:
        if not self.image:
            return ""

        return info.context.request.build_absolute_uri(self.image_optimized.url)


@strawberry.type
class SponsorsByLevel:
    level: str
    sponsors: list[Sponsor]
    highlight_color: str | None

    @classmethod
    def from_model(cls, level: SponsorLevelModel) -> Self:
        sponsors = [sponsor for sponsor in level.sponsors.all()]
        return cls(
            level=level.name, sponsors=sponsors, highlight_color=level.highlight_color
        )


@strawberry.type
class SponsorBenefit:
    name: str
    category: str
    description: str


@strawberry.type
class SponsorLevelBenefit:
    category: str
    name: str
    value: str
    description: str


@strawberry.type
class SponsorLevel:
    name: str
    price: Decimal
    slots: int | None
    benefits: list[SponsorLevelBenefit]


@strawberry.type
class SponsorSpecialOption:
    name: str
    price: Decimal
    description: str
