from django.urls import path
from healthchecks.views import health

urlpatterns = [
    path("health/", health, name="health"),
]
