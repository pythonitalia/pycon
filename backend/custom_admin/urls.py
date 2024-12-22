from custom_admin.views import astro_proxy, DjangoAdminGraphQLView
from api.schema import schema
from django.views.decorators.csrf import csrf_exempt

from django.urls import path


urlpatterns = [
    path(
        "admin/graphql",
        csrf_exempt(DjangoAdminGraphQLView.as_view(schema=schema)),
        name="django-admin-graphql",
    ),
    path("astro/<path:path>", astro_proxy, name="astro-proxy"),
]
