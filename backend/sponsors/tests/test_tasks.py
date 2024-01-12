from django.urls import reverse
from django.core.signing import Signer
import pytest
from sponsors.tasks import notify_new_sponsor_lead_via_slack, send_sponsor_brochure
from sponsors.tests.factories import SponsorLeadFactory

pytestmark = pytest.mark.django_db


def test_send_sponsor_brochure_task(sent_emails):
    sponsor_lead = SponsorLeadFactory()

    signer = Signer()
    view_brochure_path = reverse("view-brochure", args=[sponsor_lead.id])
    signed_url = signer.sign(view_brochure_path)
    signature = signed_url.split(signer.sep)[-1]

    send_sponsor_brochure(sponsor_lead.id)

    email = sent_emails[0]
    assert email["template"] == "sponsorship-brochure"
    assert email["to"] == sponsor_lead.email
    assert email["reply_to"] == ["sponsor@pycon.it"]
    assert (
        email["subject"]
        == f'[{sponsor_lead.conference.name.localize("en")}] Our Sponsorship Brochure'
    )

    assert f"{view_brochure_path}?sh={signature}" in email["variables"]["brochurelink"]


def test_notify_new_sponsor_lead_via_slack(mocker):
    mock_send_message = mocker.patch("sponsors.tasks.slack.send_message")
    sponsor_lead = SponsorLeadFactory(
        conference__slack_new_sponsor_lead_incoming_webhook_url="https://example.com"
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
    assert mock_kwargs["token"] == "https://example.com"
