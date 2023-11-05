from wagtail import blocks


class HomeIntroSection(blocks.StructBlock):
    pretitle = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)

    class Meta:
        label = "Homepage: Intro section"
        icon = "crosshairs"
