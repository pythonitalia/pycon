from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from api.schema import schema
from api.views import GraphQLView
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
    path("admin/", admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql"),
    path("user/", include("users.urls")),
    path("cms-admin/", include(wagtailadmin_urls)),
    path("cms-documents/", include(wagtaildocs_urls)),
    path("", include("association_membership.urls")),
    path("", include("healthchecks.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
