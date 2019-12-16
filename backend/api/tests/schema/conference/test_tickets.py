from api.pretix.types import TicketItem
from pytest import mark


@mark.django_db
def test_returns_tickets(graphql_client, conference, mocker):
    get_tickets_mock = mocker.patch("api.conferences.types.get_conference_tickets")
    get_tickets_mock.return_value = [
        TicketItem(
            name="Example Ticket",
            id="1",
            description="",
            active=True,
            default_price="100.00",
            variations=[],
            available_from=None,
            available_until=None,
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
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["tickets"] == [{"name": "Example Ticket"}]
