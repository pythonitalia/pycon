from wagtail import blocks


class SocialsSection(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    hashtag = blocks.CharBlock(required=True)

    class Meta:
        label = "Socials Section"
        icon = "crosshairs"
