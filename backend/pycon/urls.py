from api.schema import schema
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from strawberry.contrib.django.views import GraphQLView


# TMP:
def _debug(request):
    text = f"full path: {request.get_full_path()}\n"
    text += f"absolute url: {request.build_absolute_uri('/')}\n"

    for key, value in request.headers.items():
        text += f"{key}: {value}\n"

    return HttpResponse(f"<pre>{text}")


urlpatterns = [
    path("_dbg/", _debug),
    path("admin/", admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql"),
    path("user/", include("users.urls")),
    path("", include("social_django.urls", namespace="social")),
    path("", include("payments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
