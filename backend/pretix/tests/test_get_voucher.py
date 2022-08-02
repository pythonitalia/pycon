from django.test import override_settings
from pytest import mark

from pretix import get_voucher

pytestmark = mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_voucher(conference_factory, requests_mock, pretix_voucher_data):
    conference = conference_factory()

    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/extended-vouchers/TRYR6CWFKQHL2WGN/",
        json=pretix_voucher_data,
    )

    voucher = get_voucher(conference, "TRYR6CWFKQHL2WGN")
    assert voucher.code == "TRYR6CWFKQHL2WGN"
    assert voucher.variation_id is None
    assert voucher.items == [2]
    assert voucher.max_usages == 1
    assert not voucher.all_items


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_voucher_with_no_quota_and_item_id_is_marked_as_all_items(
    pretix_voucher_data, conference_factory, requests_mock
):
    pretix_voucher_data["item"] = None
    pretix_voucher_data["quota"] = None
    pretix_voucher_data["quota_items"] = None

    conference = conference_factory()
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/extended-vouchers/TRYR6CWFKQHL2WGN/",
        json=pretix_voucher_data,
    )

    voucher = get_voucher(conference, "TRYR6CWFKQHL2WGN")
    assert voucher.code == "TRYR6CWFKQHL2WGN"
    assert voucher.items == []
    assert voucher.all_items


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_voucher_with_quota_items(
    pretix_voucher_data, conference_factory, requests_mock
):
    pretix_voucher_data["item"] = None
    pretix_voucher_data["quota"] = 1
    pretix_voucher_data["quota_items"] = [1, 4, 5]

    conference = conference_factory()
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/extended-vouchers/TRYR6CWFKQHL2WGN/",
        json=pretix_voucher_data,
    )

    voucher = get_voucher(conference, "TRYR6CWFKQHL2WGN")
    assert voucher.code == "TRYR6CWFKQHL2WGN"
    assert voucher.items == [1, 4, 5]
    assert not voucher.all_items


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_voucher_with_invalid_code(conference_factory, requests_mock):
    conference = conference_factory()
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/extended-vouchers/TRYR6CWFKQHL2WGN/",
        status_code=404,
    )

    voucher = get_voucher(conference, "TRYR6CWFKQHL2WGN")
    assert voucher is None
