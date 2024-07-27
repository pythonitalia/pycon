from conferences.tests.factories import ConferenceFactory
from pytest import mark

from api.pretix.types import TicketItem


@mark.django_db
def test_returns_tickets(graphql_client, mocker):
    get_tickets_mock = mocker.patch("api.conferences.types.get_conference_tickets")
    get_tickets_mock.return_value = [
        TicketItem(
            name="Example Ticket",
            category="student",
            language="en",
            category_internal_name=None,
            id="1",
            description="",
            active=True,
            admission=True,
            default_price="100.00",
            tax_rate=0.0,
            variations=[],
            available_from=None,
            available_until=None,
            questions=[],
            quantity_left=0,
            sold_out=False,
        )
    ]

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                tickets(language: "en") {
                    name
                }
            }
        }
        """,
        variables={"code": ConferenceFactory().code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["tickets"] == [{"name": "Example Ticket"}]


@mark.django_db
def test_is_business(graphql_client, mocker):
    get_tickets_mock = mocker.patch("api.conferences.types.get_conference_tickets")
    get_tickets_mock.return_value = [
        TicketItem(
            name="Business Ticket",
            category="student",
            language="en",
            category_internal_name=None,
            id="1",
            description="",
            active=True,
            admission=True,
            default_price="100.00",
            tax_rate=0.0,
            variations=[],
            available_from=None,
            available_until=None,
            questions=[],
            sold_out=False,
            quantity_left=0,
        ),
        TicketItem(
            name="Normal Ticket",
            category="student",
            language="en",
            category_internal_name=None,
            id="2",
            description="",
            active=True,
            admission=True,
            default_price="100.00",
            tax_rate=0.0,
            variations=[],
            available_from=None,
            available_until=None,
            quantity_left=0,
            sold_out=False,
            questions=[],
        ),
    ]

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                tickets(language: "en") {
                    type
                }
            }
        }
        """,
        variables={"code": ConferenceFactory().code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["tickets"] == [
        {"type": "BUSINESS"},
        {"type": "STANDARD"},
    ]
