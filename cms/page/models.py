from page.blocks.sponsors_section import SponsorsSection
from home.blocks.home_intro_section import HomeIntroSection
from page.blocks.keynoters_section import KeynotersSection
from page.blocks.schedule_preview_section import SchedulePreviewSection
from page.blocks.socials_section import SocialsSection
from page.blocks.special_guest_section import SpecialGuestSection
from page.blocks.information_section import InformationSection
from news.blocks.news_grid_section import NewsGridSection
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from wagtail.fields import StreamField

from page.blocks.text_section import TextSection
from page.blocks.slider_cards_section import SliderCardsSection
from page.blocks.checkout_section import CheckoutSection
from base.blocks.map import Map
from wagtail import blocks


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


class GenericPage(Page):
    body = StreamField(
        BodyBlock(),
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
