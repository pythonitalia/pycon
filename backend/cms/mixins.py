from django.http import HttpRequest
from wagtail_headless_preview.models import HeadlessMixin, get_client_root_url_from_site


class CustomHeadlessMixin(HeadlessMixin):
    def get_client_root_url(self, request: HttpRequest) -> str:
        return get_client_root_url_from_site(self.get_site())
