from django.urls import path

from dashboard.views import dashboard

urlpatterns = [
    path("<str:conference_code>", dashboard, name="dashboard-conference"),
]
