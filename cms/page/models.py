from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from wagtail.fields import StreamField

from page.blocks.text_section import TextSection
from page.blocks.slider_cards_section import SliderCardsSection
from base.blocks.map import Map
from wagtail import blocks


class BodyBlock(blocks.StreamBlock):
    text_section = TextSection()
    map = Map()
    slider_cards_section = SliderCardsSection()


class GenericPage(Page):
    body = StreamField(
        BodyBlock(),
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
