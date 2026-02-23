from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks


class Community(blocks.StructBlock):
    name = blocks.CharBlock(required=True)
    description = blocks.RichTextBlock(required=True)
    logo = ImageChooserBlock(required=True)
    banner_photo = ImageChooserBlock(required=False)
    banner_background_color = blocks.CharBlock(required=False)

    mastodon_url = blocks.URLBlock(required=False)
    facebook_url = blocks.URLBlock(required=False)
    instagram_url = blocks.URLBlock(required=False)
    linkedin_url = blocks.URLBlock(required=False)
    twitter_url = blocks.URLBlock(required=False)


class CommunitiesSection(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    communities = blocks.ListBlock(Community)

    class Meta:
        label = "Communities Section"
        icon = "crosshairs"
