from django.urls import reverse
from django.core.signing import Signer

from unittest.mock import patch
from uuid import uuid4
import requests
from notifications.models import EmailTemplateIdentifier
from grants.tests.factories import GrantFactory
from grants.models import Grant
from visa.models import (
    InvitationLetterDocumentInclusionPolicy,
    InvitationLetterRequestStatus,
)
import pytest
from django.test import override_settings
from visa.tasks import (
    notify_new_invitation_letter_request_on_slack,
    process_invitation_letter_request,
    process_invitation_letter_request_failed,
    send_invitation_letter_via_email,
)
from visa.tests.factories import (
    InvitationLetterAssetFactory,
    InvitationLetterDocumentFactory,
    InvitationLetterConferenceConfigFactory,
    InvitationLetterRequestFactory,
)
from pypdf import PdfReader

pytestmark = pytest.mark.django_db


@pytest.fixture()
def mock_ticket_present(requests_mock):
    def _mock_ticket_present(request):
        requests_mock.get(
            "https://example.com/ticket.pdf",
            content=open("visa/tests/fixtures/sample-ticket.pdf", "rb").read(),
        )
        requests_mock.get(
            f"https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/tickets/attendee-tickets/?attendee_email={request.requester.email}",
            json=[
                {
                    "item": {
                        "admission": False,
                    }
                },
                {
                    "item": {
                        "admission": True,
                    },
                    "downloads": [{"url": "https://example.com/ticket.pdf"}],
                },
            ],
        )

    return _mock_ticket_present


@override_settings(PRETIX_API="https://pretix/api/")
def test_process_invitation_letter_request(requests_mock, mock_ticket_present):
    config = InvitationLetterConferenceConfigFactory()
    InvitationLetterAssetFactory(
        invitation_letter_conference_config=config, identifier="test"
    )
    InvitationLetterDocumentFactory(
        invitation_letter_conference_config=config,
    )
    InvitationLetterDocumentFactory(
        invitation_letter_conference_config=config,
        document=None,
        dynamic_document={
            "header": {"content": "header", "margin": "0", "align": "top-left"},
            "footer": {"content": "footer", "margin": "0", "align": "bottom-left"},
            "page_layout": {"margin": "0"},
            "pages": [
                {"content": "page: {{nationality}}"},
                {"content": 'page2: {% invitation_letter_asset "test" width="60px" %}'},
            ],
        },
    )
    # skipped as it is empty
    InvitationLetterDocumentFactory(
        invitation_letter_conference_config=config, document=None, dynamic_document=None
    )

    request = InvitationLetterRequestFactory(
        conference=config.conference, nationality="Italian"
    )
    mock_ticket_present(request)

    requests_mock.get(
        "https://example.com/ticket.pdf",
        content=open("visa/tests/fixtures/sample-ticket.pdf", "rb").read(),
    )
    requests_mock.get(
        f"https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/tickets/attendee-tickets/?attendee_email={request.requester.email}",
        json=[
            {
                "item": {
                    "admission": False,
                }
            },
            {
                "item": {
                    "admission": True,
                },
                "downloads": [{"url": "https://example.com/ticket.pdf"}],
            },
        ],
    )

    process_invitation_letter_request(invitation_letter_request_id=request.id)

    request.refresh_from_db()

    assert request.status == InvitationLetterRequestStatus.PROCESSED

    output = PdfReader(request.invitation_letter.open())
    # 1 page from the static document + 2 pages from the dynamic document + 1 page from the ticket
    assert output.get_num_pages() == 4
    assert output.pages[0].extract_text() == "Thisisasamplepdf"
    assert output.pages[1].extract_text() == "page: Italian \nheader\nfooter"
    assert output.pages[2].extract_text() == "page2: \nheader\nfooter"
    assert output.pages[3].extract_text() == "Thisisasampleticket pdf"


@pytest.mark.parametrize(
    "grant_approved_type",
    [None, Grant.ApprovedType.ticket_only, Grant.ApprovedType.ticket_travel],
)
@override_settings(PRETIX_API="https://pretix/api/")
def test_process_invitation_letter_request_accomodation_doc_with_no_accommodation(
    mock_ticket_present, grant_approved_type
):
    config = InvitationLetterConferenceConfigFactory()
    InvitationLetterDocumentFactory(
        invitation_letter_conference_config=config,
        document=None,
        dynamic_document={
            "header": {"content": "header", "margin": "0", "align": "top-left"},
            "footer": {"content": "footer", "margin": "0", "align": "bottom-left"},
            "page_layout": {"margin": "0"},
            "pages": [
                {"content": "accommodation details"},
            ],
        },
        inclusion_policy=InvitationLetterDocumentInclusionPolicy.GRANT_ACCOMMODATION,
    )

    request = InvitationLetterRequestFactory(
        conference=config.conference, nationality="Italian"
    )
    mock_ticket_present(request)

    if grant_approved_type:
        GrantFactory(
            conference=config.conference,
            user=request.requester,
            approved_type=grant_approved_type,
        )

    process_invitation_letter_request(invitation_letter_request_id=request.id)

    request.refresh_from_db()

    assert request.status == InvitationLetterRequestStatus.PROCESSED

    output = PdfReader(request.invitation_letter.open())
    assert output.get_num_pages() == 1
    assert output.pages[0].extract_text() == "Thisisasampleticket pdf"


@override_settings(PRETIX_API="https://pretix/api/")
def test_process_invitation_letter_request_with_doc_only_for_accommodation(
    mock_ticket_present,
):
    config = InvitationLetterConferenceConfigFactory()
    InvitationLetterDocumentFactory(
        invitation_letter_conference_config=config,
        document=None,
        dynamic_document={
            "header": {"content": "header", "margin": "0", "align": "top-left"},
            "footer": {"content": "footer", "margin": "0", "align": "bottom-left"},
            "page_layout": {"margin": "0"},
            "pages": [
                {"content": "accommodation details"},
            ],
        },
        inclusion_policy=InvitationLetterDocumentInclusionPolicy.GRANT_ACCOMMODATION,
    )

    request = InvitationLetterRequestFactory(
        conference=config.conference, nationality="Italian"
    )
    mock_ticket_present(request)

    GrantFactory(
        conference=config.conference,
        user=request.requester,
        approved_type=Grant.ApprovedType.ticket_travel_accommodation,
    )

    process_invitation_letter_request(invitation_letter_request_id=request.id)

    request.refresh_from_db()

    assert request.status == InvitationLetterRequestStatus.PROCESSED

    output = PdfReader(request.invitation_letter.open())
    assert output.get_num_pages() == 2
    assert output.pages[0].extract_text() == "accommodation details \nheader\nfooter"
    assert output.pages[1].extract_text() == "Thisisasampleticket pdf"


@override_settings(PRETIX_API="https://pretix/api/")
def test_process_invitation_letter_request_handles_generating_ticket_pdfs(
    requests_mock, mocker
):
    mock_time = mocker.patch("visa.tasks.time")
    config = InvitationLetterConferenceConfigFactory()

    request = InvitationLetterRequestFactory(conference=config.conference)

    requests_mock.get(
        f"https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/tickets/attendee-tickets/?attendee_email={request.requester.email}",
        json=[
            {
                "item": {
                    "admission": False,
                }
            },
            {
                "item": {
                    "admission": True,
                },
                "downloads": [{"url": "https://example.com/ticket.pdf"}],
            },
        ],
    )

    requests_mock.register_uri(
        "GET",
        "https://example.com/ticket.pdf",
        [
            {"status_code": 409, "text": "Conflict"},
            {"status_code": 409, "text": "Conflict"},
            {
                "status_code": 200,
                "content": open("visa/tests/fixtures/sample-ticket.pdf", "rb").read(),
            },
        ],
    )

    process_invitation_letter_request(invitation_letter_request_id=request.id)

    request.refresh_from_db()

    assert request.status == InvitationLetterRequestStatus.PROCESSED

    output = PdfReader(request.invitation_letter.open())

    assert output.get_num_pages() == 1

    mock_time.sleep.assert_has_calls(
        [
            mocker.call(2),
            mocker.call(4),
        ]
    )


@override_settings(PRETIX_API="https://pretix/api/")
def test_process_invitation_letter_request_handles_failing_ticket_pdfs(
    requests_mock, mocker
):
    mock_time = mocker.patch("visa.tasks.time")
    config = InvitationLetterConferenceConfigFactory()

    request = InvitationLetterRequestFactory(conference=config.conference)

    requests_mock.get(
        f"https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/tickets/attendee-tickets/?attendee_email={request.requester.email}",
        json=[
            {
                "item": {
                    "admission": False,
                }
            },
            {
                "item": {
                    "admission": True,
                },
                "downloads": [{"url": "https://example.com/ticket.pdf"}],
            },
        ],
    )

    requests_mock.register_uri(
        "GET",
        "https://example.com/ticket.pdf",
        [
            {"status_code": 409, "text": "Conflict"},
            {"status_code": 409, "text": "Conflict"},
            {"status_code": 409, "text": "Conflict"},
            {"status_code": 409, "text": "Conflict"},
            {"status_code": 409, "text": "Conflict"},
            {"status_code": 409, "text": "Conflict"},
            {
                "status_code": 200,
                "content": open("visa/tests/fixtures/sample-ticket.pdf", "rb").read(),
            },
        ],
    )

    with pytest.raises(requests.exceptions.HTTPError):
        process_invitation_letter_request(invitation_letter_request_id=request.id)

    request.refresh_from_db()

    assert not request.invitation_letter

    mock_time.sleep.assert_has_calls(
        [
            mocker.call(2),
            mocker.call(4),
            mocker.call(6),
        ]
    )


@override_settings(PRETIX_API="https://pretix/api/")
def test_process_invitation_letter_request_does_nothing_for_processed_reqs():
    config = InvitationLetterConferenceConfigFactory()

    request = InvitationLetterRequestFactory(
        conference=config.conference,
        status=InvitationLetterRequestStatus.PROCESSED,
    )

    process_invitation_letter_request(invitation_letter_request_id=request.id)

    request.refresh_from_db()
    assert request.status == InvitationLetterRequestStatus.PROCESSED


def test_process_invitation_letter_request_failed():
    request = InvitationLetterRequestFactory()

    process_invitation_letter_request_failed(
        None,
        ValueError("some error"),
        uuid4(),
        (),
        {"invitation_letter_request_id": request.id},
        None,
    )

    request.refresh_from_db()

    assert request.status == InvitationLetterRequestStatus.FAILED_TO_GENERATE


def test_notify_new_invitation_letter_request_on_slack(mocker):
    mock_slack = mocker.patch("visa.tasks.slack.send_message")
    invitation_letter_request = InvitationLetterRequestFactory(
        conference__slack_new_invitation_letter_request_channel_id="S123",
        conference__organizer__slack_oauth_bot_token="token123",
    )
    admin_absolute_uri = (
        "http://example.com/admin/visa/invitationletterrequest/1/change/"
    )

    notify_new_invitation_letter_request_on_slack(
        invitation_letter_request_id=invitation_letter_request.id,
        admin_absolute_uri=admin_absolute_uri,
    )

    mock_slack.assert_called_once()

    kwargs = mock_slack.mock_calls[0][2]
    assert kwargs["oauth_token"] == "token123"
    assert kwargs["channel_id"] == "S123"


def test_send_invitation_letter_via_email():
    invitation_letter_request = InvitationLetterRequestFactory(
        requester__full_name="Marco",
    )

    with patch("visa.tasks.EmailTemplate") as mock_email_template:
        send_invitation_letter_via_email(
            invitation_letter_request_id=invitation_letter_request.id
        )

    mock_email_template.objects.for_conference.assert_called_once_with(
        invitation_letter_request.conference
    )
    mock_email_template.objects.for_conference().get_by_identifier.assert_called_once_with(
        EmailTemplateIdentifier.visa_invitation_letter_download
    )

    signer = Signer()
    url_path = reverse(
        "download-invitation-letter", args=[invitation_letter_request.id]
    )
    signed_url = signer.sign(url_path)
    signature = signed_url.split(signer.sep)[-1]

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient_email=invitation_letter_request.email,
        placeholders={
            "invitation_letter_download_url": f"https://admin.pycon.it{url_path}?sig={signature}",
            "has_grant": False,
            "user_name": "Marco",
        },
    )

    invitation_letter_request.refresh_from_db()

    assert invitation_letter_request.status == InvitationLetterRequestStatus.SENT
