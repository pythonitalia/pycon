from billing.tests.factories import BillingAddressFactory
from billing.models import BillingAddress
from conferences.tests.factories import ConferenceFactory
import pytest
from django.test import override_settings

from pretix.exceptions import PretixError


def _create_order(graphql_client, code, input):
    return graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on CreateOrderErrors {
                    errors {
                        nonFieldErrors
                        invoiceInformation {
                            name
                            street
                            zipcode
                            fiscalCode
                            company
                            vatId
                            city
                            country
                            sdi
                            city
                            pec
                        }
                    }
                }
            }
        }""",
        variables={
            "code": code,
            "input": input,
        },
    )


def test_cannot_create_order_unlogged(graphql_client):
    conference = ConferenceFactory()
    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "",
                "fiscalCode": "GNLNCH22T27L523A",
            },
            "locale": "en",
        },
    )

    assert response["errors"][0]["message"] == "User not logged in"


@override_settings(FRONTEND_URL="http://test.it")
def test_calls_create_order(graphql_client, user, mocker):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "",
                "fiscalCode": "GNLNCH22T27L523A",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "https://example.com?return_url=http://test.it/en/orders/123/confirmation"
    )

    create_order_mock.assert_called_once()

    billing_address = BillingAddress.objects.get(user=user)

    assert billing_address.user_name == "Patrick"
    assert billing_address.company_name == ""
    assert not billing_address.is_business
    assert billing_address.address == "street"
    assert billing_address.zip_code == "92100"
    assert billing_address.city == "Avellino"
    assert billing_address.country == "IT"
    assert billing_address.vat_id == ""
    assert billing_address.fiscal_code == "GNLNCH22T27L523A"


@override_settings(FRONTEND_URL="http://test.it")
def test_handles_payment_url_set_to_none(graphql_client, user, mocker):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    # this happens when the order is free
    create_order_mock.return_value.payment_url = None
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "",
                "fiscalCode": "GNLNCH22T27L523A",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "http://test.it/en/orders/123/confirmation"
    )

    create_order_mock.assert_called_once()


def test_handles_errors(graphql_client, user, mocker):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.side_effect = PretixError("Example")

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "",
                "fiscalCode": "GNLNCH22T27L523A",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["errors"]["nonFieldErrors"] == ["Example"]

    create_order_mock.assert_called_once()


@override_settings(FRONTEND_URL="http://test.it")
@pytest.mark.parametrize(
    "field_to_remove",
    ["fiscalCode", "zipcode"],
)
def test_invoice_validation_fails_without_required_field_in_country_italy(
    graphql_client, user, mocker, field_to_remove
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    data = {
        "isBusiness": False,
        "company": "",
        "name": "Patrick",
        "street": "street",
        "zipcode": "92100",
        "city": "Avellino",
        "country": "IT",
        "vatId": "",
        "fiscalCode": "123",
    }
    data[field_to_remove] = ""

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
            "invoiceInformation": data,
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"][
        field_to_remove
    ] == ["This field is required"]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
@pytest.mark.parametrize(
    "field_to_delete", ["name", "street", "zipcode", "city", "country"]
)
def test_invoice_validation_fails_with_missing_required_fields(
    graphql_client, user, mocker, field_to_delete
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    data = {
        "isBusiness": False,
        "company": "",
        "name": "Patrick",
        "street": "street",
        "zipcode": "92100",
        "city": "Avellino",
        "country": "GB",
        "vatId": "",
        "fiscalCode": "",
    }
    data[field_to_delete] = ""

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
            "invoiceInformation": data,
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"][
        field_to_delete
    ] == ["This field is required"]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_fiscal_code_not_required_for_non_it_orders(graphql_client, user, mocker):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "GB",
                "vatId": "",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderResult"

    create_order_mock.assert_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_fails_with_invalid_fiscal_code_in_country_italy(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "",
                "fiscalCode": "PRLM3197T27B340D",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"][
        "fiscalCode"
    ] == ["Invalid fiscal code"]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_checks_pec_email_if_provided(graphql_client, user, mocker):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "",
                "fiscalCode": "",
                "pec": "invalid",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"]["pec"] == [
        "Invalid PEC address"
    ]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_fails_with_empty_vat_for_businesses(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "business",
                "name": "Patrick",
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"]["vatId"] == [
        "This field is required"
    ]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_fails_with_empty_business_name_for_businesses(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "",
                "name": "Patrick",
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "123",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"][
        "company"
    ] == ["This field is required"]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_fails_with_invalid_country_code(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "name",
                "name": "Patrick",
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "XX",
                "vatId": "123",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"][
        "country"
    ] == ["Invalid country"]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_fails_when_italian_business_and_no_sdi(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "LTD",
                "name": "Patrick",
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "123",
                "sdi": "",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"]["sdi"] == [
        "This field is required"
    ]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_fails_when_italian_business_with_invalid_sdi(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "LTD",
                "name": "Patrick",
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "IT",
                "vatId": "123",
                "sdi": "111AA",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"]["sdi"] == [
        "SDI code must be 7 characters long"
    ]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_fails_when_italian_zipcode_is_invalid(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "LTD",
                "name": "Patrick",
                "street": "street",
                "zipcode": "921",
                "city": "Avellino",
                "country": "IT",
                "vatId": "123",
                "sdi": "",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "CreateOrderErrors"
    assert response["data"]["createOrder"]["errors"]["invoiceInformation"][
        "zipcode"
    ] == ["ZIP code must be 5 characters long"]

    create_order_mock.assert_not_called()


@override_settings(FRONTEND_URL="http://test.it")
def test_invoice_validation_works_when_not_italian_and_no_sdi(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "LTD",
                "name": "Patrick",
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "GB",
                "vatId": "123",
                "sdi": "",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "https://example.com?return_url=http://test.it/en/orders/123/confirmation"
    )

    create_order_mock.assert_called()

    billing_address = BillingAddress.objects.get(user=user)

    assert billing_address.user_name == "Patrick"
    assert billing_address.company_name == "LTD"
    assert billing_address.is_business


@override_settings(FRONTEND_URL="http://test.it")
def test_create_order_billing_address_stores_both_non_and_business(
    graphql_client, user, mocker
):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    existing_billing_address = BillingAddressFactory(
        user=user,
        organizer=conference.organizer,
        is_business=False,
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "LTD",
                "name": "Patrick",
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "GB",
                "vatId": "123",
                "sdi": "",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "https://example.com?return_url=http://test.it/en/orders/123/confirmation"
    )

    create_order_mock.assert_called()

    billing_addresses = BillingAddress.objects.filter(user=user)

    assert len(billing_addresses) == 2

    assert billing_addresses.get(is_business=False).id == existing_billing_address.id

    billing_address = billing_addresses.get(is_business=True)

    assert billing_address.user_name == "Patrick"
    assert billing_address.company_name == "LTD"
    assert billing_address.is_business


@override_settings(FRONTEND_URL="http://test.it")
def test_create_order_updates_billing_address(graphql_client, user, mocker):
    conference = ConferenceFactory()
    graphql_client.force_login(user)

    existing_billing_address = BillingAddressFactory(
        user=user,
        organizer=conference.organizer,
        is_business=True,
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = _create_order(
        graphql_client,
        code=conference.code,
        input={
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
                "isBusiness": True,
                "company": "LTD",
                "name": "Patrick",
                "street": "street",
                "zipcode": "92100",
                "city": "Avellino",
                "country": "GB",
                "vatId": "123",
                "sdi": "",
                "fiscalCode": "",
            },
            "locale": "en",
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "https://example.com?return_url=http://test.it/en/orders/123/confirmation"
    )

    create_order_mock.assert_called()

    billing_address = BillingAddress.objects.get(user=user)

    assert billing_address.id == existing_billing_address.id
    assert billing_address.user_name == "Patrick"
    assert billing_address.company_name == "LTD"
    assert billing_address.is_business
