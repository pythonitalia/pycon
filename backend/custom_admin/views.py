from api.context import Context
from strawberry.django.views import GraphQLView
import re
from django.http import HttpResponse
import requests
from urllib.parse import urlparse
from django.http import QueryDict
from django.conf import settings

LOCAL_ASTRO_HTTP = "http://custom-admin:3002"


def astro_proxy(request, path):
    if not settings.DEBUG:
        return HttpResponse("Not Found", status=404)

    url = f"{LOCAL_ASTRO_HTTP}/{path}"

    requests_args = {}
    headers = get_headers(request.META)
    params = request.GET.copy()

    if "headers" not in requests_args:
        requests_args["headers"] = {}
    if "data" not in requests_args:
        requests_args["data"] = request.body
    if "params" not in requests_args:
        requests_args["params"] = QueryDict("", mutable=True)

    # Overwrite any headers and params from the incoming request with explicitly
    # specified values for the requests library.
    headers.update(requests_args["headers"])
    params.update(requests_args["params"])

    # If there's a content-length header from Django, it's probably in all-caps
    # and requests might not notice it, so just remove it.
    for key in list(headers.keys()):
        if key.lower() == "content-length":
            del headers[key]

    requests_args["headers"] = headers
    requests_args["params"] = params

    response = requests.request(request.method, url, **requests_args)
    content = response.content.decode("utf-8")

    # Base path doesn't seem to be fully supported by Astro
    # so we need to manually fix all the references to the root
    content = content.replace('type="module" src="/', 'type="module" src="/astro/')
    content = content.replace('from "/', 'from "/astro/')
    content = content.replace('import "/', 'import "/astro/')
    content = content.replace('import("/', 'import("/astro/')
    content = content.replace('renderer-url="/', 'renderer-url="/astro/')
    content = content.replace(
        'before-hydration-url="/', 'before-hydration-url="/astro/'
    )
    content = content.replace('component-url="/', 'component-url="/astro/')
    # if you are changing this line below, make sure the HMR proxy
    # in ws.py is also updated as we also need
    # to change the paths in the HMR messages
    content = content.replace(
        '__vite__createHotContext("/', '__vite__createHotContext("/astro/'
    )

    proxy_response = HttpResponse(content, status=response.status_code)

    excluded_headers = set(
        [
            # Hop-by-hop headers
            # ------------------
            # Certain response headers should NOT be just tunneled through.  These
            # are they.  For more info, see:
            # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
            "connection",
            "keep-alive",
            "proxy-authenticate",
            "proxy-authorization",
            "te",
            "trailers",
            "transfer-encoding",
            "upgrade",
            # Although content-encoding is not listed among the hop-by-hop headers,
            # it can cause trouble as well.  Just let the server set the value as
            # it should be.
            "content-encoding",
            # Since the remote server may or may not have sent the content in the
            # same encoding as Django will, let Django worry about what the length
            # should be.
            "content-length",
        ]
    )
    for key, value in response.headers.items():
        if key.lower() in excluded_headers:
            continue
        elif key.lower() == "location":
            # If the location is relative at all, we want it to be absolute to
            # the upstream server.
            proxy_response[key] = make_absolute_location(response.url, value)
        else:
            proxy_response[key] = value

    return proxy_response


def make_absolute_location(base_url, location):
    absolute_pattern = re.compile(r"^[a-zA-Z]+://.*$")
    if absolute_pattern.match(location):
        return location

    parsed_url = urlparse(base_url)

    if location.startswith("//"):
        # scheme relative
        return parsed_url.scheme + ":" + location

    elif location.startswith("/"):
        # host relative
        return parsed_url.scheme + "://" + parsed_url.netloc + location

    else:
        # path relative
        return (
            parsed_url.scheme
            + "://"
            + parsed_url.netloc
            + parsed_url.path.rsplit("/", 1)[0]
            + "/"
            + location
        )

    return location


def get_headers(environ):
    """
    Retrieve the HTTP headers from a WSGI environment dictionary.  See
    https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
    """
    headers = {}
    for key, value in environ.items():
        # Sometimes, things don't like when you send the requesting host through.
        if key.startswith("HTTP_") and key != "HTTP_HOST":
            headers[key[5:].replace("_", "-")] = value
        elif key in ("CONTENT_TYPE", "CONTENT_LENGTH"):
            headers[key.replace("_", "-")] = value

    return headers


class DjangoAdminGraphQLView(GraphQLView):
    allow_queries_via_get = False

    def get_context(self, request, response) -> Context:
        return Context(request=request, response=response)
