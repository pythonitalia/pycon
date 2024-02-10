from custom_admin.views import astro_proxy
from django_admin_api.views import DjangoAdminGraphQLView
from django_admin_api.schema import schema as django_admin_graphql_schema
from django.contrib.admin.views.decorators import staff_member_required

from django.urls import path


urlpatterns = [
    path(
        "admin/graphql",
        staff_member_required(
            DjangoAdminGraphQLView.as_view(schema=django_admin_graphql_schema)
        ),
        name="django-admin-graphql",
    ),
    path("astro/<path:path>", staff_member_required(astro_proxy), name="astro-proxy"),
]
