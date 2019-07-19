from api.views import GraphQLView
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view())),
    path("user/", include("users.urls")),
    path("", include("social_django.urls", namespace="social")),
    path("", include("payments.urls")),
]
