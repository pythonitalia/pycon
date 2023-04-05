from base.blocks.cta import CTA
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class SpecialGuestSection(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    guest_name = blocks.CharBlock(required=True)
    guest_photo = ImageChooserBlock(required=True)
    guest_job_title = blocks.CharBlock(required=True)
    event_date = blocks.DateBlock(required=True)

    cta = CTA()

    class Meta:
        label = "Special Guest Section"
        icon = "crosshairs"
