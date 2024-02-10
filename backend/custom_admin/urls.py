from custom_admin.views import astro_proxy, DjangoAdminGraphQLView
from api.schema import schema
from django.contrib.admin.views.decorators import staff_member_required

from django.urls import path


urlpatterns = [
    path(
        "admin/graphql",
        DjangoAdminGraphQLView.as_view(schema=schema),
        name="django-admin-graphql",
    ),
    path("astro/<path:path>", staff_member_required(astro_proxy), name="astro-proxy"),
]
