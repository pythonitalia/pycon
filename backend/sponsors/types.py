import typing

import strawberry


@strawberry.type
class Sponsor:
    level: str
    name: str

    @strawberry.field
    def link(self, info) -> typing.Optional[str]:
        if self.link != "":
            return self.link

    @strawberry.field
    def image(self, info) -> typing.Optional[str]:
        if not self.image:
            return None

        return info.context["request"].build_absolute_uri(self.image.url)


@strawberry.type
class SponsorsByLevel:
    level: str
    sponsors: typing.List[Sponsor]
