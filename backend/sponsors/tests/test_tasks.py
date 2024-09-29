from unittest.mock import patch
from django.urls import reverse
from django.core.signing import Signer
import pytest
from sponsors.tasks import notify_new_sponsor_lead_via_slack, send_sponsor_brochure
from sponsors.tests.factories import SponsorLeadFactory

pytestmark = pytest.mark.django_db


def test_send_sponsor_brochure_task():
    sponsor_lead = SponsorLeadFactory()

    signer = Signer()
    view_brochure_path = reverse("view-brochure", args=[sponsor_lead.id])
    signed_url = signer.sign(view_brochure_path)
    signature = signed_url.split(signer.sep)[-1]

    with patch("sponsors.tasks.EmailTemplate") as mock_email_template:
        send_sponsor_brochure(sponsor_lead.id)

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient_email=sponsor_lead.email,
        placeholders={
            "brochure_url": f"https://admin.pycon.it{view_brochure_path}?sig={signature}",
            "conference_name": sponsor_lead.conference.name.localize("en"),
        },
    )


def test_notify_new_sponsor_lead_via_slack(mocker):
    mock_send_message = mocker.patch("sponsors.tasks.slack.send_message")
    sponsor_lead = SponsorLeadFactory(
        conference__slack_new_sponsor_lead_channel_id="c123"
    )

    notify_new_sponsor_lead_via_slack(
        sponsor_lead_id=sponsor_lead.id, admin_absolute_uri="http://localhost:8000/"
    )

    mock_send_message.assert_called_once()
    mock_args = mock_send_message.call_args.args
    assert (
        f"/admin/sponsors/sponsorlead/{sponsor_lead.id}/change/"
        in mock_args[1][0]["blocks"][0]["elements"][0]["url"]
    )
    mock_kwargs = mock_send_message.call_args.kwargs
    assert mock_kwargs["channel_id"] == "c123"
