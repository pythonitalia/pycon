from django.urls import reverse
from django.core.signing import Signer
import pytest
from sponsors.tasks import send_sponsor_brochure
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
