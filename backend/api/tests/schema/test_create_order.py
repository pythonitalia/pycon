from pretix.exceptions import PretixError


def test_calls_create_order(graphql_client, user, conference, mocker):
    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                ... on CreateOrderResult {
                    paymentUrl
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [
                    {
                        "ticketId": "1",
                        "attendeeName": "ABC",
                        "attendeeEmail": "patrick.arminio@gmail.com",
                        "variation": "1",
                        "answers": [{"questionId": "1", "value": "Example"}],
                    }
                ],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "https://example.com?return_url=http://localhost:4000/en/orders"
        "/123/confirmation"
    )

    create_order_mock.assert_called_once()


def test_handles_errors(graphql_client, user, conference, mocker):
    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.side_effect = PretixError("Example")

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [
                    {
                        "attendeeName": "ABC",
                        "attendeeEmail": "patrick.arminio@gmail.com",
                        "ticketId": "1",
                        "variation": "1",
                    }
                ],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["message"] == "Example"

    create_order_mock.assert_called_once()
