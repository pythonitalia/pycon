from django.conf import settings

from wagtail.wagtailcore.middleware import SiteMiddleware
from wagtail.wagtailredirects.middleware import RedirectMiddleware



class CustomSiteMiddleware(SiteMiddleware):
    def process_request(self, request):
        if request_uses_wagtail(request.path):
            super().process_request(request)



class CustomRedirectMiddleware(RedirectMiddleware):
    def process_response(self, request, response):
        if request_uses_wagtail(request.path):
            return super().process_response(request, response)

        return response


def request_uses_wagtail(path):
    if not path:
        return False

    for url in settings.WAGTAIL_EXCLUDE_URLS:
        if url in path:
            return False

    return True
