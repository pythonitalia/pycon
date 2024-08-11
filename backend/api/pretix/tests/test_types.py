import pytest
from api.pretix.types import AttendeeNameInput


def test_validate_attendee_name():
    input = AttendeeNameInput(
        parts={"given_name": "John", "family_name": "Doe"}, scheme="given_family"
    )

    assert input.validate()


def test_validate_attendee_name_with_empty_family_name():
    input = AttendeeNameInput(
        parts={"given_name": "John", "family_name": ""}, scheme="given_family"
    )

    assert not input.validate()


def test_validate_attendee_name_with_empty_given_name():
    input = AttendeeNameInput(
        parts={"given_name": "", "family_name": "Doe"}, scheme="given_family"
    )

    assert not input.validate()


@pytest.mark.parametrize("value", ["", " "])
def test_validate_attendee_name_with_invalid_legacy_name(value):
    input = AttendeeNameInput(
        parts={
            "_legacy": value,
        },
        scheme="legacy",
    )

    assert not input.validate()


def test_validate_attendee_name_with_valid_legacy_name():
    input = AttendeeNameInput(
        parts={
            "_legacy": "Hello",
        },
        scheme="legacy",
    )

    assert input.validate()


def test_validate_attendee_name_with_no_parts_is_invalid():
    input = AttendeeNameInput(parts={}, scheme="legacy")

    assert not input.validate()
