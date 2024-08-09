from organizers.tests.factories import OrganizerFactory
from billing.tests.factories import BillingAddressFactory
from conferences.tests.factories import ConferenceFactory
import pytest

pytestmark = pytest.mark.django_db


def _query_billing_addresses(graphql_client, code):
    return graphql_client.query(
        """query($conference: String!) {
        me {
            billingAddresses(conference: $conference) {
                id
                isBusiness
                companyName
                userName
                zipCode
                city
                address
                country
                vatId
                fiscalCode
                sdi
                pec
            }
        }
    }""",
        variables={
            "conference": code,
        },
    )


def test_fetch_user_billing_addresses(graphql_client, user):
    conference = ConferenceFactory()

    address_1 = BillingAddressFactory(
        user=user,
        organizer=conference.organizer,
    )

    BillingAddressFactory(
        user=user,
        organizer=OrganizerFactory(),
    )

    BillingAddressFactory(
        organizer=conference.organizer,
    )

    graphql_client.force_login(user)

    response = _query_billing_addresses(graphql_client, conference.code)

    assert not response.get("errors")
    addresses = response["data"]["me"]["billingAddresses"]
    assert len(addresses) == 1
    assert addresses[0]["id"] == str(address_1.id)


def test_fetch_user_billing_addresses_with_no_addresses(graphql_client, user):
    conference = ConferenceFactory()

    BillingAddressFactory(
        organizer=conference.organizer,
    )

    graphql_client.force_login(user)

    response = _query_billing_addresses(graphql_client, conference.code)

    assert not response.get("errors")
    addresses = response["data"]["me"]["billingAddresses"]
    assert len(addresses) == 0
