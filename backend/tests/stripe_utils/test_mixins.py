import pytest

from stripe_utils.mixins import StripeCustomerMixin


def test_mixin_without_customer_id():
    with pytest.raises(NotImplementedError):
        x = StripeCustomerMixin()


def test_mixin_with_customer_id():
    class Example(StripeCustomerMixin):
        customer_id = 123

    x = Example()
