from wagtail import blocks


class Accordion(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    is_open = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        icon = "arrow-down"
