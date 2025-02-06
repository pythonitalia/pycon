from django.urls import path

from visa.views import download_invitation_letter

urlpatterns = [
    path(
        "download-invitation-letter/<int:id>",
        download_invitation_letter,
        name="download-invitation-letter",
    ),
]
