from typing import Self
import strawberry
from api.cms.page.registry import register_page_block


@strawberry.type
class Community:
    name: str
    description: str
    logo: str | None
    banner_photo: str | None
    banner_background_color: str | None

    mastodon_url: str | None
    facebook_url: str | None
    instagram_url: str | None
    linkedin_url: str | None
    twitter_url: str | None

    @classmethod
    def from_block(cls, block) -> Self:
        logo_url = None
        if block["logo"]:
            logo_url = block["logo"].get_rendition("width-300|jpegquality-60").full_url

        banner_photo_url = None
        if block["banner_photo"]:
            banner_photo_url = (
                block["banner_photo"].get_rendition("width-300|jpegquality-60").full_url
            )

        return cls(
            name=block["name"],
            description=block["description"],
            logo=logo_url,
            banner_photo=banner_photo_url,
            banner_background_color=block["banner_background_color"],
            mastodon_url=block["mastodon_url"],
            facebook_url=block["facebook_url"],
            instagram_url=block["instagram_url"],
            linkedin_url=block["linkedin_url"],
            twitter_url=block["twitter_url"],
        )


@register_page_block()
@strawberry.type
class CommunitiesSection:
    id: strawberry.ID
    title: str
    communities: list[Community]

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            title=block.value["title"],
            communities=[
                Community.from_block(community)
                for community in block.value["communities"]
            ],
        )
