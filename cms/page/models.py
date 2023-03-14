from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from wagtail.fields import StreamField

from page.blocks import BodyBlock


class GenericPage(Page):
    body = StreamField(
        BodyBlock(),
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
