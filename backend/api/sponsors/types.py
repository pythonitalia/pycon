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


@strawberry_django.type(models.SponsorLevelBenefit)
class SponsorLevelBenefit:
    category: str = strawberry_django.field(
        resolver=lambda self: self.benefit.category,
        select_related=["benefit"],
    )
    name: str = strawberry_django.field(
        resolver=lambda self: self.benefit.name,
        select_related=["benefit"],
    )
    value: str = strawberry_django.field(only=["value"])
    description: str = strawberry_django.field(
        resolver=lambda self: self.benefit.description,
        select_related=["benefit"],
    )


@strawberry_django.type(models.SponsorLevel)
class SponsorLevel:
    name: strawberry.auto
    price: strawberry.auto
    slots: int | None
    benefits: list[SponsorLevelBenefit] = strawberry_django.field(
        field_name="sponsorlevelbenefit_set"
    )


@strawberry_django.type(models.SponsorSpecialOption)
class SponsorSpecialOption:
    name: strawberry.auto
    price: strawberry.auto
    description: strawberry.auto
