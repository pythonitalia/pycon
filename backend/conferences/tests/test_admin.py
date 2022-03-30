from unittest.mock import call

import time_machine
from django.core import exceptions
from django.forms.fields import BooleanField
from django.utils import timezone
from pytest import fixture, mark, raises

from conferences.admin import DeadlineForm, validate_deadlines_form
from conferences.models import SpeakerVoucher
from schedule.admin import send_voucher_via_email
from schedule.models import ScheduleItem

pytestmark = mark.django_db


@fixture(autouse=False)
def add_delete_field_to_form():
    DeadlineForm.base_fields["DELETE"] = BooleanField(required=False)
    yield
    del DeadlineForm.base_fields["DELETE"]


def test_can_have_multiple_deadlines_only_if_the_other_are_deleted(
    conference_factory, add_delete_field_to_form
):
    conference = conference_factory()
    form_1 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2022-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "cfp",
            "conference": conference.id,
            "DELETE": False,
        }
    )
    form_2 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2023-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "cfp",
            "conference": conference.id,
            "DELETE": True,
        }
    )

    form_1.is_valid()
    form_2.is_valid()

    forms = [form_1, form_2]

    validate_deadlines_form(forms)


@mark.parametrize("type", ["cfp", "voting", "refund"])
def test_cannot_have_duplicate_deadlines(
    conference_factory, type, add_delete_field_to_form
):
    conference = conference_factory()
    form_1 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2022-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": type,
            "conference": conference.id,
            "DELETE": False,
        }
    )
    form_2 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2023-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": type,
            "conference": conference.id,
            "DELETE": False,
        }
    )

    form_1.is_valid()
    form_2.is_valid()

    forms = [form_1, form_2]

    with raises(
        exceptions.ValidationError,
        match=f"You can only have one deadline of type {type}",
    ):
        validate_deadlines_form(forms)


def test_start_date_comes_before_end(conference_factory, add_delete_field_to_form):
    conference = conference_factory()
    form_1 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2020-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "cfp",
            "conference": conference.id,
            "DELETE": False,
        }
    )

    form_1.is_valid()

    forms = [form_1]

    with raises(exceptions.ValidationError, match="Start date cannot be after end"):
        validate_deadlines_form(forms)


def test_can_have_as_many_custom_deadlines_as_we_want(
    conference_factory, add_delete_field_to_form
):
    conference = conference_factory()
    form_1 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2022-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "custom",
            "conference": conference.id,
            "DELETE": False,
        }
    )
    form_2 = DeadlineForm(
        data={
            "start": "2021-11-10 01:43:58",
            "end": "2023-11-10 01:43:58",
            "name_0": "en",
            "name_1": "it",
            "description_0": "descen",
            "description_1": "descit",
            "type": "custom",
            "conference": conference.id,
            "DELETE": False,
        }
    )

    form_1.is_valid()
    form_2.is_valid()

    forms = [form_1, form_2]

    validate_deadlines_form(forms)


@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_send_voucher_via_email(
    rf,
    schedule_item_factory,
    conference_factory,
    submission_factory,
    speaker_voucher_factory,
    mocker,
):
    mocker.patch("schedule.admin.messages")
    mock_send_email = mocker.patch("schedule.admin.send_speaker_voucher_email")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=600),
    )

    speaker_voucher_1 = speaker_voucher_factory(
        conference=conference,
        user_id=500,
        pretix_voucher_id=1,
    )
    speaker_voucher_2 = speaker_voucher_factory(
        conference=conference,
        user_id=600,
        pretix_voucher_id=2,
    )

    send_voucher_via_email(
        None, rf.get("/"), queryset=SpeakerVoucher.objects.filter(conference=conference)
    )

    mock_send_email.assert_has_calls(
        [
            call(speaker_voucher_1),
            call(speaker_voucher_2),
        ]
    )

    speaker_voucher_1.refresh_from_db()
    speaker_voucher_2.refresh_from_db()

    assert speaker_voucher_1.voucher_email_sent_at == timezone.now()
    assert speaker_voucher_2.voucher_email_sent_at == timezone.now()


@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_send_voucher_via_email_requires_filtering_by_conference(
    rf,
    schedule_item_factory,
    conference_factory,
    submission_factory,
    speaker_voucher_factory,
    mocker,
):
    mock_messages = mocker.patch("schedule.admin.messages")
    mock_send_email = mocker.patch("schedule.admin.send_speaker_voucher_email")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    conference_2 = conference_factory(pretix_speaker_voucher_quota_id=123)

    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference_2,
        submission=submission_factory(conference=conference_2, speaker_id=600),
    )

    speaker_voucher_1 = speaker_voucher_factory(
        conference=conference,
        user_id=500,
        pretix_voucher_id=1,
    )
    speaker_voucher_2 = speaker_voucher_factory(
        conference=conference_2,
        user_id=600,
        pretix_voucher_id=2,
    )

    request = rf.get("/")
    send_voucher_via_email(
        None,
        request,
        queryset=SpeakerVoucher.objects.filter(
            conference__in=[conference, conference_2]
        ),
    )

    mock_messages.error.assert_called_once_with(
        request, "Please select only one conference"
    )
    mock_send_email.assert_not_called()

    speaker_voucher_1.refresh_from_db()
    speaker_voucher_2.refresh_from_db()

    assert speaker_voucher_1.voucher_email_sent_at is None
    assert speaker_voucher_2.voucher_email_sent_at is None
