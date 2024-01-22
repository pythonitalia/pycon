from wagtail.models import Page
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail_headless_preview.models import HeadlessMixin


class NewsArticle(HeadlessMixin, Page):
    excerpt = models.TextField(max_length=255)
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("excerpt"),
        FieldPanel("body"),
        FieldPanel("first_published_at"),
    ]
