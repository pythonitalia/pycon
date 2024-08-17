import pytest
from api.pretix.types import AttendeeNameInput, UpdateAttendeeTicketErrors


def test_validate_attendee_name():
    errors = UpdateAttendeeTicketErrors()

    input = AttendeeNameInput(
        parts={"given_name": "John", "family_name": "Doe"}, scheme="given_family"
    )

    with errors.with_prefix("attendee_name"):
        input.validate(errors)

    assert not errors.has_errors


def test_validate_attendee_name_with_empty_family_name():
    errors = UpdateAttendeeTicketErrors()

    input = AttendeeNameInput(
        parts={"given_name": "John", "family_name": ""}, scheme="given_family"
    )

    with errors.with_prefix("attendee_name"):
        input.validate(errors)

    assert errors.has_errors
    assert errors.errors.attendee_name.family_name == ["This field may not be blank."]
    assert errors.errors.attendee_name.given_name == []


def test_validate_attendee_name_with_empty_given_name():
    errors = UpdateAttendeeTicketErrors()

    input = AttendeeNameInput(
        parts={"given_name": "", "family_name": "Doe"}, scheme="given_family"
    )

    with errors.with_prefix("attendee_name"):
        input.validate(errors)

    assert errors.has_errors
    assert errors.errors.attendee_name.given_name == ["This field may not be blank."]
    assert errors.errors.attendee_name.family_name == []


@pytest.mark.parametrize("value", ["", " "])
def test_validate_attendee_name_with_invalid_legacy_name(value):
    errors = UpdateAttendeeTicketErrors()

    input = AttendeeNameInput(
        parts={
            "_legacy": value,
        },
        scheme="legacy",
    )

    with errors.with_prefix("attendee_name"):
        input.validate(errors)

    assert errors.has_errors
    assert errors.errors.attendee_name.non_field_errors == [
        "This field may not be blank."
    ]
    assert errors.errors.attendee_name.given_name == []
    assert errors.errors.attendee_name.family_name == []


def test_validate_attendee_name_with_valid_legacy_name():
    errors = UpdateAttendeeTicketErrors()

    input = AttendeeNameInput(
        parts={
            "_legacy": "Hello",
        },
        scheme="legacy",
    )

    with errors.with_prefix("attendee_name"):
        input.validate(errors)

    assert not errors.has_errors


def test_validate_attendee_name_with_no_parts_is_invalid():
    errors = UpdateAttendeeTicketErrors()

    input = AttendeeNameInput(parts={}, scheme="legacy")

    with errors.with_prefix("attendee_name"):
        input.validate(errors)

    assert errors.has_errors
    assert errors.errors.attendee_name.non_field_errors == [
        "This field may not be blank."
    ]
