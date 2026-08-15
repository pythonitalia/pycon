from cms.components.base.blocks.cta import CTA
from wagtail import blocks


class HomepageHero(blocks.StructBlock):
    city = blocks.ChoiceBlock(
        choices=[
            ("florence", "Florence"),
            ("bologna", "Bologna"),
        ]
    )
    title = blocks.CharBlock(
        required=False,
        help_text="The conference name as text, e.g. 'PyCon Italia 2027'.",
    )
    location = blocks.CharBlock(
        required=False,
        help_text="Where the conference happens, e.g. 'Bologna'.",
    )
    dates = blocks.CharBlock(
        required=False,
        help_text="When the conference happens, e.g. 'May 27 - 30, 2027'.",
    )
    subtitle = blocks.CharBlock(
        required=False,
        help_text=(
            "One line describing the kind of event, e.g. 'Four days of talks, "
            "tutorials and community, in Bologna'."
        ),
    )
    highlight = blocks.CharBlock(
        required=False,
        help_text="Optional credibility marker, e.g. '1,000+ attendees'.",
    )
    primary_cta = CTA(label="Primary CTA")
    secondary_cta = CTA(label="Secondary CTA")

    class Meta:
        label = "Homepage Hero"
        icon = "crosshairs"
