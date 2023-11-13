from cms.components.base.blocks.cta import CTA
from wagtail import blocks


class SchedulePreviewSection(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    primary_cta = CTA(label="Primary CTA")
    secondary_cta = CTA(label="Secondary CTA")

    class Meta:
        label = "Schedule Preview Section"
        icon = "crosshairs"
