from wagtail.signals import page_published
from django.apps import AppConfig


class PageConfig(AppConfig):
    name = "page"

    def ready(self):
        from . import signals

        page_published.connect(signals.revalidate_pycon_frontend)
