from wagtail import blocks
from cms.components.base.blocks.cta import CTA


class SimpleTextCard(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    cta = CTA()

    class Meta:
        label = "Card: Simple Text"
        icon = "doc-full"


class PriceCard(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    price = blocks.CharBlock()
    price_tier = blocks.CharBlock()
    cta = CTA()

    class Meta:
        label = "Card: Price"
        icon = "doc-full"


class SliderCardsSection(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
    )
    spacing = blocks.ChoiceBlock(
        default="xl",
        choices=[
            ("xl", "Extra Large"),
            ("3xl", "3 Extra Large"),
        ],
    )
    snake_background = blocks.BooleanBlock(required=False, default=False)
    cards = blocks.StreamBlock(
        [
            ("simple_text_card", SimpleTextCard()),
            ("price_card", PriceCard()),
        ]
    )

    class Meta:
        label = "Slider Cards Section"
        icon = "crosshairs"
