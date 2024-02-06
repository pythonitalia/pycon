from custom_admin.views import astro_proxy
from django_admin_api.views import DjangoAdminGraphQLView
from django_admin_api.schema import schema as django_admin_graphql_schema

from django.urls import path


urlpatterns = [
    path(
        "admin/graphql",
        DjangoAdminGraphQLView.as_view(schema=django_admin_graphql_schema),
        name="django-admin-graphql",
    ),
    path("astro/<path:path>", astro_proxy, name="astro-proxy"),
]
