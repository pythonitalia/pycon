from django.test import override_settings
from pretix.db import get_orders_status


@override_settings(SIMULATE_PRETIX_DB=True)
def test_no_order_status_when_the_db_is_simulated():
    assert get_orders_status(["A"]) == {}


@override_settings(SIMULATE_PRETIX_DB=False)
def test_get_order_statuses(mocker):
    connections_mock = mocker.patch("pretix.db.connections")
    connections_mock.__getitem__.return_value.cursor.return_value.__enter__.return_value.fetchall.return_value = (  # noqa
        ("A", "p"),
        ("B", "c"),
        ("C", "n"),
    )

    statuses = get_orders_status(["A", "B", "C"])

    assert statuses == {"A": "p", "B": "c", "C": "n"}
