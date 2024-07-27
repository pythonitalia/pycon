from users.tests.factories import UserFactory
from conferences.tests.factories import ConferenceFactory
from schedule.tests.factories import (
    ScheduleItemAdditionalSpeakerFactory,
    ScheduleItemFactory,
)
from submissions.tests.factories import SubmissionFactory
import pytest

from newsletters.exporter import convert_user_to_endpoint

pytestmark = pytest.mark.skip(reason="disabled export for now")


def test_converts_one_user():
    user = UserFactory()

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == []
    assert endpoint.has_item_in_schedule == []
    assert endpoint.has_cancelled_talks == []


def test_adds_submissions_sent():
    conference = ConferenceFactory()
    user = UserFactory()

    SubmissionFactory(speaker_id=user.id, conference=conference)

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == [conference.code]
    assert endpoint.has_item_in_schedule == []
    assert endpoint.has_cancelled_talks == []


def test_adds_items_in_schedule():
    conference = ConferenceFactory()
    user = UserFactory()

    submission = SubmissionFactory(speaker_id=user.id, conference=conference)
    ScheduleItemFactory(type="submission", submission=submission, conference=conference)

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == [conference.code]
    assert endpoint.has_item_in_schedule == [conference.code]
    assert endpoint.has_cancelled_talks == []


def test_adds_items_in_schedule_even_if_additional_speaker():
    conference = ConferenceFactory()
    user = UserFactory()
    additional_user = UserFactory()

    submission = SubmissionFactory(speaker_id=user.id, conference=conference)
    item = ScheduleItemFactory(
        type="submission", submission=submission, conference=conference
    )
    ScheduleItemAdditionalSpeakerFactory(scheduleitem=item, user_id=additional_user.id)

    endpoint = convert_user_to_endpoint(additional_user)

    assert endpoint.id == str(additional_user.id)
    assert endpoint.name == additional_user.name
    assert endpoint.full_name == additional_user.full_name
    assert endpoint.is_staff == additional_user.is_staff
    assert endpoint.has_sent_submission_to == []
    assert endpoint.has_item_in_schedule == [conference.code]
    assert endpoint.has_cancelled_talks == []


def test_has_list_of_talks_per_conference():
    conference = ConferenceFactory()
    user = UserFactory()

    submission = SubmissionFactory(speaker_id=user.id, conference=conference)
    item = ScheduleItemFactory(
        type="submission", submission=submission, conference=conference
    )

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == [conference.code]
    assert endpoint.has_item_in_schedule == [conference.code]
    assert endpoint.has_cancelled_talks == []
    assert endpoint.talks_by_conference == {conference.code: [item.title]}


def test_adds_cancelled_talks():
    conference = ConferenceFactory()
    user = UserFactory()

    SubmissionFactory(speaker_id=user.id, conference=conference, status="cancelled")

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == [conference.code]
    assert endpoint.has_item_in_schedule == []
    assert endpoint.has_cancelled_talks == [conference.code]
