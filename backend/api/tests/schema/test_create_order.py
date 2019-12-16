def test_calls_create_order(graphql_client, user, conference, mocker):
    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"

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
                "tickets": [{"ticketId": "1", "quantity": 3, "variation": "1"}],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == "https://example.com"

    create_order_mock.assert_called_once()
