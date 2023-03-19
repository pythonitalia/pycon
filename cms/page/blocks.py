from wagtail import blocks

from wagtail.images.blocks import ImageChooserBlock


class Map(blocks.StructBlock):
    longitude = blocks.DecimalBlock(max_digits=9, decimal_places=6)
    latitude = blocks.DecimalBlock(max_digits=9, decimal_places=6)
    zoom = blocks.IntegerBlock(default=15)

    class Meta:
        icon = "map"


class TextSection(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock()
    illustration = blocks.CharBlock(required=False)

    class Meta:
        icon = "section"


class BodyBlock(blocks.StreamBlock):
    text_section = TextSection()
    map = Map()
    image = ImageChooserBlock()
