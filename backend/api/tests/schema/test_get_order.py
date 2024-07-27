from conferences.tests.factories import ConferenceFactory


def test_calls_get_order(graphql_client, user, mocker):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    get_order_mock = mocker.patch("api.pretix.query.pretix.get_order")
    get_order_mock.return_value = {
        "code": "abc",
        "status": "p",
        "url": "",
        "total": "100.00",
        "email": user.email,
    }

    response = graphql_client.query(
        """query GetOrder($conferenceCode: String!, $code: String!) {
            order(conferenceCode: $conferenceCode, code: $code) {
                code
            }
        }""",
        variables={"code": "abc", "conferenceCode": conference.code},
    )

    assert not response.get("errors")
    assert response["data"]["order"]["code"] == "abc"

    get_order_mock.assert_called_once()


def test_calls_returns_none(graphql_client, user, mocker):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    get_order_mock = mocker.patch("api.pretix.query.pretix.get_order")
    get_order_mock.return_value = None

    response = graphql_client.query(
        """query GetOrder($conferenceCode: String!, $code: String!) {
            order(conferenceCode: $conferenceCode, code: $code) {
                code
            }
        }""",
        variables={"code": "abc", "conferenceCode": conference.code},
    )

    assert not response.get("errors")
    assert response["data"]["order"] is None

    get_order_mock.assert_called_once()


def test_calls_returns_none_when_email_is_different(graphql_client, user, mocker):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    get_order_mock = mocker.patch("api.pretix.query.pretix.get_order")
    get_order_mock.return_value = {
        "code": "abc",
        "status": "p",
        "url": "",
        "total": "100.00",
        "email": "example@abc.com",
    }

    response = graphql_client.query(
        """query GetOrder($conferenceCode: String!, $code: String!) {
            order(conferenceCode: $conferenceCode, code: $code) {
                code
            }
        }""",
        variables={"code": "abc", "conferenceCode": conference.code},
    )

    assert not response.get("errors")
    assert response["data"]["order"] is None

    get_order_mock.assert_called_once()
