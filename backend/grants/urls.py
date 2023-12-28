from .views import grant_summary_view
from django.urls import path

urlpatterns = [
    path("grant-summary/", grant_summary_view, name="grant-summary"),
]
