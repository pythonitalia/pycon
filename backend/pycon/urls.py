from api.schema import schema
from api.views import GraphQLView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from submissions.views import SubmissionAutocomplete
from users.views import UserAutocomplete

urlpatterns = [
    path(
        "admin/_/user-autocomplete",
        UserAutocomplete.as_view(),
        name="user-autocomplete",
    ),
    path(
        "admin/_/submission-autocomplete",
        SubmissionAutocomplete.as_view(),
        name="submission-autocomplete",
    ),
    path("admin/", admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql"),
    path("user/", include("users.urls")),
    path("", include("social_django.urls", namespace="social")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
