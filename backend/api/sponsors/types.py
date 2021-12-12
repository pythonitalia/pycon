from __future__ import annotations

import typing

import strawberry
from strawberry import ID

from sponsors.models import SponsorLevel as SponsorLevelModel


@strawberry.type
class Sponsor:
    id: ID
    name: str

    @strawberry.field
    def link(self, info) -> typing.Optional[str]:
        if self.link != "":
            return self.link

    @strawberry.field
    def image(self, info) -> typing.Optional[str]:
        if not self.image:
            return None

        return info.context.request.build_absolute_uri(self.image.url)


@strawberry.type
class SponsorsByLevel:
    level: str
    sponsors: typing.List[Sponsor]
    highlight_color: typing.Optional[str]

    @classmethod
    def from_model(cls, level: SponsorLevelModel) -> SponsorsByLevel:
        sponsors = [sponsor for sponsor in level.sponsors.all()]
        return cls(level.name, sponsors, level.highlight_color)
