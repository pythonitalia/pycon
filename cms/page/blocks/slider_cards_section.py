from wagtail import blocks
from base.blocks.cta import CTA


class SimpleTextCard(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    cta = CTA()

    class Meta:
        label = "Card: Simple Text"
        icon = "doc-full"


class SliderCardsSection(blocks.StructBlock):
    cards = blocks.ListBlock(SimpleTextCard)

    class Meta:
        label = "Slider Cards Section"
        icon = "crosshairs"
