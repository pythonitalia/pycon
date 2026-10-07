from cms.components.base.blocks.cta import CTA
from cms.components.page.fields import IllustrationChoiceBlock
from wagtail import blocks


class HomepageHero(blocks.StructBlock):
    city = blocks.ChoiceBlock(
        choices=[
            ("florence", "Florence"),
            ("bologna", "Bologna"),
        ]
    )
    pretitle = blocks.CharBlock(
        required=False,
        help_text="When and where, e.g. 'Bologna, May 27 – 30, 2027'",
    )
    title = blocks.CharBlock(
        required=False,
        help_text="The conference name as text, e.g. 'PyCon Italia 2027'",
    )
    subtitle = blocks.CharBlock(
        required=False,
        help_text=(
            "One line describing the event, e.g. 'Four days of talks, "
            "tutorials and community, in Bologna'"
        ),
    )
    highlight = blocks.CharBlock(
        required=False,
        help_text="Optional credibility marker, e.g. '1,000+ attendees'",
    )
    primary_cta = CTA(label="Primary CTA")
    secondary_cta = CTA(label="Secondary CTA")
    illustration = IllustrationChoiceBlock(
        required=False,
        help_text=(
            "Shown next to the copy instead of the animated city illustration. "
            "Renders immediately, so prefer it when the fold has to be fast."
        ),
    )

    class Meta:
        label = "Homepage Hero"
        icon = "crosshairs"
