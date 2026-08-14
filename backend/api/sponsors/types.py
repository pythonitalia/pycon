from decimal import Decimal

import strawberry
import strawberry_django

from api.context import Info
from sponsors import models


@strawberry_django.type(models.Sponsor)
class Sponsor:
    id: strawberry.auto
    name: strawberry.auto
    link: strawberry.auto

    @strawberry_django.field(only=["image"])
    def image(self, info: Info) -> str:
        if not self.image:
            return ""

        return info.context.request.build_absolute_uri(self.image_optimized.url)


@strawberry_django.type(models.SponsorLevel)
class SponsorsByLevel:
    level: str = strawberry_django.field(field_name="name")
    sponsors: list[Sponsor]
    highlight_color: str | None


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
