from decimal import Decimal

import pytest
from payments.providers.utils import to_cents


def test_to_cents():
    amount = Decimal("10")
    assert to_cents(amount) == 1000


def test_to_cents_cannot_convert_non_deciaml_numbers():
    with pytest.raises(ValueError) as exc:
        to_cents(500)

    assert "Make sure the amount passed to `to_cents` is not already converted" in str(
        exc.value
    )
