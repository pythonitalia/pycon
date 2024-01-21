from wagtail_headless_preview.models import HeadlessMixin as BaseHeadlessMixin
from django.utils.http import urlencode


class CustomHeadlessMixin(BaseHeadlessMixin):
    def get_preview_url(self, token):
        root_url = self.get_client_root_url()
        args = urlencode({"content_type": self.get_content_type_str(), "token": token})
        return f"{root_url}api/page-preview?{args}"
