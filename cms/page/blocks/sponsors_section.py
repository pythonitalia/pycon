from base.blocks.cta import CTA
from wagtail import blocks


class SponsorsSection(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    body = blocks.CharBlock(required=True)
    cta = CTA()
    layout = blocks.ChoiceBlock(
        required=False,
        default="side-by-side",
        choices=[("side-by-side", "Side-by-side"), ("vertical", "Vertical")],
    )

    class Meta:
        label = "Sponsors Section"
        icon = "crosshairs"
