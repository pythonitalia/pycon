import pytest
from users.tests.fake_pretix import FAKE_PRETIX_ITEMS


@pytest.fixture
def pretix_items():
    return FAKE_PRETIX_ITEMS
