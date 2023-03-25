from wagtail import blocks


class CTA(blocks.StructBlock):
    label = blocks.CharBlock(required=False)
    link = blocks.CharBlock(required=False)

    class Meta:
        label = "Call to Action"
        icon = "site"
