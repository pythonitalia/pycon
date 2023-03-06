from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from wagtail.fields import StreamField
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


class GenericPage(Page):
    body = StreamField(
        [
            ("text_section", TextSection()),
            ("map", Map()),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
