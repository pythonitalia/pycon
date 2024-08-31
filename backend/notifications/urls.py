from django.urls import path
from notifications.views import sns_webhook


urlpatterns = [
    path("notifications/sns-webhook/", sns_webhook, name="sns_webhook"),
]
