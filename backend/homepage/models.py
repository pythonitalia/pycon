from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.models import Page


class HomePage(Page):
    class Meta:
        verbose_name = 'Homepage'
