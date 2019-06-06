import pytest

from pytest import mark

from decimal import Decimal


@mark.django_db
def test_order_charge_with_not_known_provider(order_factory):
    order = order_factory(amount=Decimal('4.20'), provider='undefined')

    with pytest.raises(ValueError) as e:
        order.charge({})

    assert 'Provider undefined not known' in str(e)
