from base.blocks.accordion import Accordion
from base.blocks.cta import CTA
from page.fields import IllustrationChoiceBlock
from wagtail import blocks


class TextSection(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    is_main_title = blocks.BooleanBlock(required=False, default=False)
    subtitle = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    body_text_size = blocks.ChoiceBlock(
        required=False,
        default="text-1",
        choices=[("text-1", "Text-1"), ("text-2", "Text-2")],
    )
    illustration = IllustrationChoiceBlock(
        required=False,
    )
    accordions = blocks.ListBlock(Accordion)
    cta = CTA()

    class Meta:
        icon = "doc-full"
