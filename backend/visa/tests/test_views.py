import pytest
from django.core.signing import Signer
from visa.models import InvitationLetterRequestStatus
from visa.tests.factories import (
    InvitationLetterRequestFactory,
    SentInvitationLetterRequestFactory,
)
from pytest import mark
from django.urls import reverse

pytestmark = mark.django_db


def test_download_invitation_letter_without_signature_fails(client):
    invitation_letter_request = InvitationLetterRequestFactory(
        status=InvitationLetterRequestStatus.SENT
    )
    response = client.get(
        reverse("download-invitation-letter", args=[invitation_letter_request.id])
    )

    assert response.status_code == 403
    assert response.content.decode() == "Missing signature."


def test_download_invitation_letter_with_invalid_signature_fails(client):
    signer = Signer()
    signature = signer.sign("something-else").split(signer.sep)[-1]

    invitation_letter_request = InvitationLetterRequestFactory(
        status=InvitationLetterRequestStatus.SENT
    )
    response = client.get(
        reverse("download-invitation-letter", args=[invitation_letter_request.id])
        + f"?sig={signature}"
    )

    assert response.status_code == 403
    assert response.content.decode() == "Invalid signature."


def test_download_invitation_letter(client):
    invitation_letter_request = SentInvitationLetterRequestFactory()

    url_path = reverse(
        "download-invitation-letter", args=[invitation_letter_request.id]
    )

    signer = Signer()
    signature = signer.sign(url_path).split(signer.sep)[-1]
    response = client.get(url_path + f"?sig={signature}")

    assert response.status_code == 302
    assert response.url == invitation_letter_request.invitation_letter.url


@pytest.mark.parametrize(
    "status",
    [
        InvitationLetterRequestStatus.PENDING,
        InvitationLetterRequestStatus.PROCESSING,
        InvitationLetterRequestStatus.PROCESSED,
        InvitationLetterRequestStatus.FAILED_TO_GENERATE,
        InvitationLetterRequestStatus.REJECTED,
    ],
)
def test_cannot_download_non_sent_invitation_letter_request(client, status):
    invitation_letter_request = InvitationLetterRequestFactory(status=status)

    url_path = reverse(
        "download-invitation-letter", args=[invitation_letter_request.id]
    )

    signer = Signer()
    signature = signer.sign(url_path).split(signer.sep)[-1]
    response = client.get(url_path + f"?sig={signature}")

    assert response.status_code == 404
    assert (
        response.content.decode("utf-8")
        == "We can't find this invitation letter request. Please contact us."
    )


def test_cannot_download_non_existent_invitation_letter_request(client):
    invitation_letter_request = InvitationLetterRequestFactory(
        status=InvitationLetterRequestStatus.REJECTED
    )

    url_path = reverse(
        "download-invitation-letter", args=[invitation_letter_request.id]
    )

    signer = Signer()
    signature = signer.sign(url_path).split(signer.sep)[-1]

    invitation_letter_request.delete()

    response = client.get(url_path + f"?sig={signature}")

    assert response.status_code == 404
    assert (
        response.content.decode("utf-8")
        == "We can't find this invitation letter request. Please contact us."
    )
