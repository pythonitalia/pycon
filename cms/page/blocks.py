from wagtail import blocks

from wagtail.images.blocks import ImageChooserBlock


class Accordion(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    is_open = blocks.BooleanBlock(require=False, default=True)

    class Meta:
        icon = "arrow-down"


class Map(blocks.StructBlock):
    longitude = blocks.DecimalBlock(max_digits=9, decimal_places=6)
    latitude = blocks.DecimalBlock(max_digits=9, decimal_places=6)
    zoom = blocks.IntegerBlock(default=15)

    class Meta:
        icon = "globe"


class TextSection(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock()
    illustration = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("snakeTail", "Snake Tail"),
            ("snakeHead", "Snake Head"),
            ("snakesWithSigns", "Snakes with Signs"),
        ],
        icon="image",
    )

    class Meta:
        icon = "doc-full"


class TextSectionWithAccordion(TextSection):
    accordions = blocks.ListBlock(Accordion)

    class Meta:
        icon = "doc-full-inverse"


class BodyBlock(blocks.StreamBlock):
    text_section = TextSection()
    map = Map()
    image = ImageChooserBlock()
    text_section_with_accordion = TextSectionWithAccordion()
