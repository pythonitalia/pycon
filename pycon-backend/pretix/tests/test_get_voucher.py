from django.test import override_settings
from pretix.db import get_voucher
from pytest import mark


@override_settings(SIMULATE_PRETIX_DB=True)
def test_no_voucher_is_found_if_the_db_is_simulated():
    assert get_voucher("slug", "code") is None


@override_settings(SIMULATE_PRETIX_DB=False)
def test_get_voucher_with_invalid_code(mocker):
    connections_mock = mocker.patch("pretix.db.connections")
    connections_mock.__getitem__.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value = ()  # noqa

    assert get_voucher("slug", "code") is None


@override_settings(SIMULATE_PRETIX_DB=False)
def test_get_voucher(mocker):
    connections_mock = mocker.patch("pretix.db.connections")
    connections_mock.__getitem__.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value = (
        1,
        "code",
        None,
        "50.00",
        5,
        0,
        2,
        "set",
        None,
        None,
    )  # noqa

    voucher = get_voucher("slug", "code")

    assert voucher.code == "code"
    assert voucher.price_mode == "set"
    assert voucher.value == "50.00"
    assert voucher.max_usages == 2
    assert voucher.items == [5]


@override_settings(SIMULATE_PRETIX_DB=False)
def test_get_voucher_with_no_quota_and_item_id_is_marked_as_all_items(mocker):
    connections_mock = mocker.patch("pretix.db.connections")
    connections_mock.__getitem__.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value = (
        1,
        "code",
        None,
        "50.00",
        None,
        0,
        2,
        "set",
        None,
        None,
    )  # noqa

    voucher = get_voucher("slug", "code")

    assert voucher.code == "code"
    assert voucher.price_mode == "set"
    assert voucher.value == "50.00"
    assert voucher.max_usages == 2
    assert voucher.items == []
    assert voucher.all_items is True


@override_settings(SIMULATE_PRETIX_DB=False)
def test_get_voucher_with_quota_selects_all_items_of_the_quota(mocker):
    connections_mock = mocker.patch("pretix.db.connections")
    connections_mock.__getitem__.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value = (
        1,
        "code",
        None,
        "50.00",
        None,
        0,
        2,
        "set",
        1,
        None,
    )  # noqa
    connections_mock.__getitem__.return_value.cursor.return_value.__enter__.return_value.fetchall.return_value = (
        (1,),
        (2,),
        (3,),
    )  # noqa

    voucher = get_voucher("slug", "code")

    assert voucher.code == "code"
    assert voucher.price_mode == "set"
    assert voucher.value == "50.00"
    assert voucher.max_usages == 2
    assert voucher.items == [1, 2, 3]
    assert voucher.all_items is False
