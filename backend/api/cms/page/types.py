from typing import Self
from cms.components.page.models import GenericPage as GenericPageModel

import strawberry

from api.cms.page.blocks.slider_cards_section import SliderCardsSection
from api.cms.page.blocks.text_section import TextSection
from api.cms.base.blocks.map import CMSMap
from api.cms.home.blocks.home_intro_section import HomeIntroSection
from api.cms.page.blocks.sponsors_section import SponsorsSection
from api.cms.page.blocks.schedule_preview_section import SchedulePreviewSection
from api.cms.page.blocks.keynoters_section import KeynotersSection
from api.cms.page.blocks.socials_section import SocialsSection
from api.cms.page.blocks.special_guest_section import SpecialGuestSection
from api.cms.page.blocks.information_section import InformationSection
from api.cms.news.blocks.news_grid_section import NewsGridSection
from api.cms.page.blocks.checkout_section import CheckoutSection
from api.cms.page.blocks.live_streaming_section import LiveStreamingSection


@strawberry.type
class SiteNotFoundError:
    message: str


REGISTRY = {
    "text_section": TextSection,
    "map": CMSMap,
    "slider_cards_section": SliderCardsSection,
    "sponsors_section": SponsorsSection,
    "home_intro_section": HomeIntroSection,
    "keynoters_section": KeynotersSection,
    "schedule_preview_section": SchedulePreviewSection,
    "socials_section": SocialsSection,
    "special_guest_section": SpecialGuestSection,
    "information_section": InformationSection,
    "news_grid_section": NewsGridSection,
    "checkout_section": CheckoutSection,
    "live_streaming_section": LiveStreamingSection,
}

Block = strawberry.union(
    "Block",
    REGISTRY.values(),
)


@strawberry.type
class GenericPage:
    id: strawberry.ID
    title: str
    search_description: str
    slug: str
    body: list[Block]

    @classmethod
    def from_model(cls, obj: GenericPageModel) -> Self:
        return cls(
            id=obj.id,
            title=obj.seo_title or obj.title,
            search_description=obj.search_description,
            slug=obj.slug,
            body=[
                REGISTRY.get(block.block_type).from_block(block) for block in obj.body
            ],
        )