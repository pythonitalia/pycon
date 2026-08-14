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


@strawberry_django.type(models.SponsorBenefit)
class SponsorBenefit:
    name: str = strawberry_django.field(only=["name"])
    category: str = strawberry_django.field(only=["category"])
    description: str = strawberry_django.field(only=["description"])


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


@strawberry_django.type(models.SponsorSpecialOption)
class SponsorSpecialOption:
    name: strawberry.auto
    price: strawberry.auto
    description: strawberry.auto
