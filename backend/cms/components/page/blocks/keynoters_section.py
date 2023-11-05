from cms.components.base.blocks.cta import CTA
from wagtail import blocks


class KeynotersSection(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    cta = CTA()

    class Meta:
        label = "Keynoters Section"
        icon = "crosshairs"
