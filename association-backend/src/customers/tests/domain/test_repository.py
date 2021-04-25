from collections import namedtuple
from unittest.mock import patch

from ward import test

from src.association.tests.session import db
from src.customers.domain.entities import UserID
from src.customers.domain.repository import CustomersRepository
from src.customers.tests.factories import CustomerFactory

StripeCustomer = namedtuple("StripeCustomer", ["id"])


@test("get customer for user id")
async def _(db=db):
    customer = await CustomerFactory(user_id=1)
    repository = CustomersRepository()

    found_customer = await repository.get_for_user_id(UserID(1))

    assert found_customer.id == customer.id


@test("get customer not existent user id")
async def _(db=db):
    await CustomerFactory(user_id=1)
    repository = CustomersRepository()

    found_customer = await repository.get_for_user_id(UserID(5))

    assert found_customer is None


@test("get customer from stripe id")
async def _(db=db):
    customer = await CustomerFactory(stripe_customer_id="cus_1")
    repository = CustomersRepository()

    found_customer = await repository.get_for_stripe_customer_id("cus_1")

    assert found_customer.id == customer.id


@test("get customer from non existent stripe id")
async def _(db=db):
    await CustomerFactory(stripe_customer_id="cus_1")
    repository = CustomersRepository()

    found_customer = await repository.get_for_stripe_customer_id("cus_555")

    assert found_customer is None


@test("create stripe portal url")
async def _(db=db):
    customer = await CustomerFactory(stripe_customer_id="cus_1")

    with patch(
        "src.customers.domain.repository.stripe.billing_portal.Session.create"
    ) as mock_create:
        repository = CustomersRepository()

        mock_create.return_value.url = "https://web.url"
        stripe_portal_url = await repository.create_stripe_portal_session_url(customer)

    assert stripe_portal_url == "https://web.url"


@test("create customer and stripe customer")
async def _(db=db):
    with patch(
        "src.customers.domain.repository.stripe.Customer.create"
    ) as mock_customers_create:
        mock_customers_create.return_value.id = "cus_created"

        repository = CustomersRepository()

        created_customer = await repository.create_for_user(
            user_id=UserID(5), email="test@email.it"
        )

    mock_customers_create.assert_called_once_with(
        email="test@email.it", metadata={"user_id": 5}
    )

    assert created_customer.id is not None
    assert created_customer.stripe_customer_id == "cus_created"
