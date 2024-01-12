import pytest
from sponsors.tasks import send_sponsor_brochure
from sponsors.tests.factories import SponsorLeadFactory

pytestmark = pytest.mark.django_db


def test_send_sponsor_brochure_task(sent_emails):
    sponsor_lead = SponsorLeadFactory()

    send_sponsor_brochure(sponsor_lead.id)

    email = sent_emails[0]
    assert email["template"] == "sponsorship-brochure"
    assert email["to"] == sponsor_lead.email
    assert email["reply_to"] == ["sponsor@pycon.it"]
    assert (
        email["subject"]
        == f'[{sponsor_lead.conference.name.localize("en")}] Our Sponsorship Brochure'
    )

    assert (
        f"/sponsors/view-brochure/{sponsor_lead.id}/?sh="
        in email["variables"]["brochurelink"]
    )
