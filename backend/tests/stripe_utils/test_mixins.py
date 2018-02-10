from decimal import Decimal

import pytest
from djstripe.models import Customer

from stripe_utils.mixins import StripeCustomerMixin
from users.models import User


def test_mixin_without_customer_id():
    with pytest.raises(NotImplementedError):
        x = StripeCustomerMixin()


def test_mixin_with_customer_id():
    class Example(StripeCustomerMixin):
        customer_id = 123

    x = Example()


def test_returns_empty_orders(stripe_customer_id):
    class Example(StripeCustomerMixin):
        customer_id = stripe_customer_id

    x = Example()

    assert len(x.get_orders()) == 0


@pytest.mark.django_db
def test_stores_order(stripe_customer_id):
    user = User.objects.create_user(email='test@example.org')

    # TODO: abstract this

    customer, _ = Customer.get_or_create(user)

    x = customer.add_card('tok_visa')

    customer.charge(Decimal('10.0'))

    # assert len(x.get_orders()) == 1
