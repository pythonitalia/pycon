from conferences.tests.factories import ConferenceFactory
from pytest import mark
from sponsors.models import SponsorLead
from sponsors.tests.factories import SponsorLeadFactory

pytestmark = mark.django_db


def _send_sponsor_lead(client, input):
    return client.query(
        """mutation SendSponsorLead($input: SendSponsorLeadInput!) {
            sendSponsorLead(input: $input) {
                __typename
                ... on SendSponsorLeadInputErrors {
                    errors {
                        fullname
                        email
                        company
                        conferenceCode
                        nonFieldErrors
                    }
                }
                ... on OperationResult {
                    ok
                }
            }
        }""",
        variables={"input": input},
    )


@mark.parametrize("consent_to_contact_via_email", [True, False])
def test_send_sponsor_lead(graphql_client, consent_to_contact_via_email, mocker):
    mock_send_brochure = mocker.patch("api.sponsors.schema.send_sponsor_brochure")

    conference = ConferenceFactory()

    resp = _send_sponsor_lead(
        graphql_client,
        input={
            "fullname": "Tester",
            "email": "example@example.org",
            "company": "Example",
            "conferenceCode": conference.code,
            "consentToContactViaEmail": consent_to_contact_via_email,
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["sendSponsorLead"]["__typename"] == "OperationResult"
    assert resp["data"]["sendSponsorLead"]["ok"] is True

    sponsor_lead = SponsorLead.objects.get()
    assert sponsor_lead.email == "example@example.org"
    assert sponsor_lead.conference == conference
    assert sponsor_lead.fullname == "Tester"
    assert sponsor_lead.company == "Example"
    assert sponsor_lead.consent_to_contact_via_email is consent_to_contact_via_email
    assert sponsor_lead.brochure_viewed is False

    mock_send_brochure.delay.assert_called_once_with(sponsor_lead_id=sponsor_lead.id)


def test_send_sponsor_lead_only_sends_the_brochure_once_an_email(
    graphql_client, mocker
):
    mock_send_brochure = mocker.patch("api.sponsors.schema.send_sponsor_brochure")
    conference = ConferenceFactory()

    sponsor_lead = SponsorLeadFactory(
        fullname="Tester",
        email="example@example.org",
        company="Example",
        conference=conference,
        consent_to_contact_via_email=False,
    )

    resp = _send_sponsor_lead(
        graphql_client,
        input={
            "fullname": "Tester",
            "email": "example@example.org",
            "company": "Example",
            "conferenceCode": conference.code,
            "consentToContactViaEmail": False,
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["sendSponsorLead"]["__typename"] == "OperationResult"
    assert resp["data"]["sendSponsorLead"]["ok"] is True

    sponsor_lead.refresh_from_db()
    assert SponsorLead.objects.count() == 1

    assert sponsor_lead.email == "example@example.org"
    assert sponsor_lead.conference == conference
    assert sponsor_lead.fullname == "Tester"
    assert sponsor_lead.company == "Example"
    assert sponsor_lead.consent_to_contact_via_email is False
    assert sponsor_lead.brochure_viewed is False

    mock_send_brochure.delay.assert_not_called()


def test_send_sponsor_lead_required_fields(graphql_client):
    resp = _send_sponsor_lead(
        graphql_client,
        input={
            "fullname": "",
            "email": "",
            "company": "",
            "conferenceCode": "",
            "consentToContactViaEmail": True,
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["sendSponsorLead"]["__typename"] == "SendSponsorLeadInputErrors"
    assert resp["data"]["sendSponsorLead"]["errors"]["fullname"] == ["Required"]
    assert resp["data"]["sendSponsorLead"]["errors"]["email"] == ["Required"]
    assert resp["data"]["sendSponsorLead"]["errors"]["company"] == ["Required"]
    assert resp["data"]["sendSponsorLead"]["errors"]["conferenceCode"] == ["Required"]
    assert resp["data"]["sendSponsorLead"]["errors"]["nonFieldErrors"] == []


def test_send_sponsor_lead_with_invalid_email(graphql_client):
    conference = ConferenceFactory()

    resp = _send_sponsor_lead(
        graphql_client,
        input={
            "fullname": "Tester",
            "email": "not-an-email",
            "company": "Company",
            "conferenceCode": conference.code,
            "consentToContactViaEmail": True,
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["sendSponsorLead"]["__typename"] == "SendSponsorLeadInputErrors"
    assert resp["data"]["sendSponsorLead"]["errors"]["email"] == [
        "Invalid email address"
    ]


def test_send_sponsor_lead_invalid_conference_code(graphql_client):
    resp = _send_sponsor_lead(
        graphql_client,
        input={
            "fullname": "Tester",
            "email": "example@example.org",
            "company": "Example",
            "conferenceCode": "unknown-conf",
            "consentToContactViaEmail": True,
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["sendSponsorLead"]["__typename"] == "SendSponsorLeadInputErrors"
    assert resp["data"]["sendSponsorLead"]["errors"]["fullname"] == []
    assert resp["data"]["sendSponsorLead"]["errors"]["email"] == []
    assert resp["data"]["sendSponsorLead"]["errors"]["company"] == []
    assert resp["data"]["sendSponsorLead"]["errors"]["conferenceCode"] == [
        "Invalid conference code"
    ]
