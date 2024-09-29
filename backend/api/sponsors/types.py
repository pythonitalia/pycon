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
    def link(self, info) -> str:
        return self.link

    @strawberry.field
    def image(self, info) -> str:
        if not self.image:
            return ""

        # try:
        return info.context.request.build_absolute_uri(self.image_optimized.url)
        # except Exception as e:
        # return info.context.request.build_absolute_uri(self.image.url)


@strawberry.type
class SponsorsByLevel:
    level: str
    sponsors: typing.List[Sponsor]
    highlight_color: typing.Optional[str]

    @classmethod
    def from_model(cls, level: SponsorLevelModel) -> SponsorsByLevel:
        sponsors = [sponsor for sponsor in level.sponsors.all()]
        return cls(
            level=level.name, sponsors=sponsors, highlight_color=level.highlight_color
        )


@strawberry.type
class SponsorBrochureStats:
    attendees: str
    speakers: str
    talks: str
    unique_online_visitors: str
    sponsors_and_partners: str
    grants_given: str
    coffees: str


@strawberry.type
class SponsorBrochureText:
    text: str


@strawberry.type
class SponsorBrochureLocationText:
    city: SponsorBrochureText
    country: SponsorBrochureText


@strawberry.type
class SponsorBrochureWhySponsorText:
    introduction: SponsorBrochureText
    text: str


@strawberry.type
class SponsorBrochure:
    stats: SponsorBrochureStats
    introduction: SponsorBrochureText
    tags: SponsorBrochureText
    location: SponsorBrochureLocationText
    community: SponsorBrochureText
    why_sponsor: SponsorBrochureWhySponsorText
