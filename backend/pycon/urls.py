from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from api.schema import schema
from api.views import GraphQLView
from pycon.views import disabled_view
from submissions.views import SubmissionAutocomplete
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path(
        "admin/_/submission-autocomplete",
        SubmissionAutocomplete.as_view(),
        name="submission-autocomplete",
    ),
    path("", include("custom_admin.urls")),
    path("admin/", admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql"),
    path("user/", include("users.urls")),
    path("cms-admin/users/", disabled_view),
    path("cms-admin/", include(wagtailadmin_urls)),
    path("cms-documents/", include(wagtaildocs_urls)),
    path("", include("association_membership.urls")),
    path("integrations/", include("integrations.urls")),
    path("sponsors/", include("sponsors.urls")),
    path("schedule/", include("schedule.urls")),
    path("", include("healthchecks.urls")),
    path("", include("files_upload.urls")),
    path("", include("notifications.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG and settings.ENABLE_DJANGO_DEBUG_TOOLBAR:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()


urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
