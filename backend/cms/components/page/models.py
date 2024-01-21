from cms.components.page.blocks.homepage_hero import HomepageHero
from cms.components.page.blocks.sponsors_section import SponsorsSection
from cms.components.home.blocks.home_intro_section import HomeIntroSection
from cms.components.page.blocks.keynoters_section import KeynotersSection
from cms.components.page.blocks.schedule_preview_section import SchedulePreviewSection
from cms.components.page.blocks.socials_section import SocialsSection
from cms.components.page.blocks.special_guest_section import SpecialGuestSection
from cms.components.page.blocks.information_section import InformationSection
from cms.components.news.blocks.news_grid_section import NewsGridSection
from cms.components.page.blocks.live_streaming_section import LiveStreamingSection
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from wagtail.fields import StreamField

from cms.components.page.blocks.text_section import TextSection
from cms.components.page.blocks.slider_cards_section import SliderCardsSection
from cms.components.page.blocks.checkout_section import CheckoutSection
from cms.components.base.blocks.map import Map
from wagtail import blocks
from .headless import CustomHeadlessMixin


class BodyBlock(blocks.StreamBlock):
    text_section = TextSection()
    map = Map()
    slider_cards_section = SliderCardsSection()
    sponsors_section = SponsorsSection()

    home_intro_section = HomeIntroSection()
    keynoters_section = KeynotersSection()
    schedule_preview_section = SchedulePreviewSection()
    socials_section = SocialsSection()
    special_guest_section = SpecialGuestSection()
    information_section = InformationSection()
    news_grid_section = NewsGridSection()
    checkout_section = CheckoutSection()
    live_streaming_section = LiveStreamingSection()
    homepage_hero = HomepageHero()


class GenericPage(CustomHeadlessMixin, Page):
    body = StreamField(
        BodyBlock(),
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
