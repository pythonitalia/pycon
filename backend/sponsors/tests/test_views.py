from django.core.signing import Signer
from django.urls import reverse
import pytest
from sponsors.tests.factories import SponsorLeadFactory
from wagtail_factories import DocumentFactory


pytestmark = pytest.mark.django_db


def test_view_brochure_view_without_signature_fails(client):
    sponsor_lead = SponsorLeadFactory(brochure_viewed=False)
    response = client.get(reverse("view-brochure", args=[sponsor_lead.id]))

    assert response.status_code == 403
    assert response.content.decode() == "Invalid signature."


def test_view_brochure_view_with_wrong_signature_fails(client):
    signer = Signer()
    signature = signer.sign("something-else").split(signer.sep)[-1]

    sponsor_lead = SponsorLeadFactory(brochure_viewed=False)
    response = client.get(
        reverse("view-brochure", args=[sponsor_lead.id]) + f"?sh={signature}"
    )

    assert response.status_code == 403
    assert response.content.decode() == "Invalid signature."


def test_view_brochure_view(client):
    sponsor_lead = SponsorLeadFactory(brochure_viewed=False, conference__code="code")
    brochure = DocumentFactory()
    brochure.tags.add("sponsorship-brochure", sponsor_lead.conference.code)

    view_brochure_url_path = reverse("view-brochure", args=[sponsor_lead.id])
    signer = Signer()
    signature = signer.sign(view_brochure_url_path).split(signer.sep)[-1]

    response = client.get(view_brochure_url_path + f"?sh={signature}")

    assert response.status_code == 302
    assert response.url == brochure.url

    sponsor_lead.refresh_from_db()
    assert sponsor_lead.brochure_viewed is True
