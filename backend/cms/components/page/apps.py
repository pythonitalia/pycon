from wagtail.signals import page_published
from django.apps import AppConfig


class PageConfig(AppConfig):
    name = "cms.components.page"

    def ready(self):
        from . import signals

        page_published.connect(signals.revalidate_vercel_frontend)
