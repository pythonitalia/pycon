from cms.components.base.blocks.cta import CTA
from wagtail import blocks


class HomepageHero(blocks.StructBlock):
    city = blocks.ChoiceBlock(
        choices=[
            ("florence", "Florence"),
            ("bologna", "Bologna"),
        ]
    )
    variant = blocks.ChoiceBlock(
        required=False,
        default="illustration_only",
        choices=[
            ("illustration_only", "Illustration only"),
            ("overlay", "Overlay (copy on top of the illustration)"),
        ],
        help_text=(
            "Illustration only keeps the full-screen illustration with no text. "
            "Overlay puts the copy and the CTAs below on top of it."
        ),
    )
    title = blocks.CharBlock(
        required=False,
        label="Title",
        help_text="The conference name as text, e.g. PyCon Italia 2027.",
    )
    subtitle = blocks.CharBlock(
        required=False,
        label="Dates and city",
        help_text="e.g. Bologna, May 27 - 30, 2027.",
    )
    body = blocks.CharBlock(
        required=False,
        label="One line description",
        help_text=(
            "What kind of event this is, in one line, e.g. Four days of talks, "
            "tutorials and community, in Bologna."
        ),
    )
    highlight = blocks.CharBlock(
        required=False,
        label="Scale",
        help_text="Optional credibility marker, e.g. 1,000+ attendees.",
    )
    primary_cta = CTA(label="Primary CTA")
    secondary_cta = CTA(label="Secondary CTA")

    class Meta:
        label = "Homepage Hero"
        icon = "crosshairs"
