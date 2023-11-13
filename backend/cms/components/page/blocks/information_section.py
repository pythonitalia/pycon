from wagtail import blocks
from cms.components.base.blocks.cta import CTA
from cms.components.page.fields import (
    BackgroundColorChoiceBlock,
    IllustrationChoiceBlock,
)


class InformationSection(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
    )
    body = blocks.RichTextBlock(required=False)
    illustration = IllustrationChoiceBlock(
        required=False,
    )
    background_color = BackgroundColorChoiceBlock(required=True)
    countdown_to_datetime = blocks.DateTimeBlock(required=False)
    countdown_to_deadline = blocks.CharBlock(required=False)

    cta = CTA()

    class Meta:
        label = "Information Section"
        icon = "crosshairs"
