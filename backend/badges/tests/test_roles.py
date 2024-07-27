from django.conf import settings
from conferences.tests.factories import ConferenceFactory
from submissions.tests.factories import SubmissionFactory
from schedule.tests.factories import (
    ScheduleItemAdditionalSpeakerFactory,
    ScheduleItemFactory,
)
from badges.roles import (
    Role,
    _get_roles,
    get_conference_roles_for_user,
    speakers_user_ids,
)
import pytest
from badges.models import AttendeeConferenceRole
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_get_all_speakers_user_ids():
    schedule_item_1 = ScheduleItemFactory(type="talk", submission=SubmissionFactory())
    schedule_item_2 = ScheduleItemFactory(
        type="talk",
        conference=schedule_item_1.conference,
        submission=SubmissionFactory(),
    )
    schedule_item_3 = ScheduleItemFactory(
        type="talk",
        conference=schedule_item_1.conference,
        submission=SubmissionFactory(),
    )
    additional_speaker = ScheduleItemAdditionalSpeakerFactory()
    schedule_item_3.additional_speakers.add(additional_speaker)

    schedule_item_different_conf = ScheduleItemFactory(
        type="talk",
        conference=ConferenceFactory(),
        submission=SubmissionFactory(),
    )

    speaker_ids = speakers_user_ids(schedule_item_1.conference)
    assert len(speaker_ids) == 4
    assert schedule_item_1.submission.speaker_id in speaker_ids
    assert schedule_item_2.submission.speaker_id in speaker_ids
    assert schedule_item_3.submission.speaker_id in speaker_ids
    assert additional_speaker.user_id in speaker_ids

    assert schedule_item_different_conf.submission.speaker_id not in speaker_ids


@pytest.mark.parametrize(
    "voucher_tag,voucher_code,expected_roles",
    (
        ("speakers", "code", [Role.SPEAKER, Role.ATTENDEE]),
        ("", "keynoter-123", [Role.KEYNOTER, Role.ATTENDEE]),
        ("staff", "code", [Role.STAFF, Role.ATTENDEE]),
        ("", "staff-5667", [Role.STAFF, Role.ATTENDEE]),
        ("sponsor,pizzacorp", "pizza", [Role.SPONSOR, Role.ATTENDEE]),
        ("community,sushi", "code", [Role.ATTENDEE]),
    ),
)
def test_get_roles(requests_mock, voucher_tag, voucher_code, expected_roles):
    conference = ConferenceFactory()
    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/vouchers",
        status_code=200,
        json={
            "next": None,
            "results": [{"id": 1, "code": voucher_code, "tag": voucher_tag}],
        },
    )

    roles = _get_roles(
        conference=conference,
        user_id=1,
        ticket={
            "id": 1,
            "voucher": 1,
        },
    )
    assert roles == expected_roles


def test_get_roles_for_speaker_without_voucher(requests_mock, submission_factory):
    conference = ConferenceFactory()

    submission = SubmissionFactory()
    ScheduleItemFactory(type="talk", conference=conference, submission=submission)

    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/vouchers",
        status_code=200,
        json={"next": None, "results": []},
    )

    roles = _get_roles(
        conference=conference,
        user_id=submission.speaker_id,
        ticket={
            "id": 1,
            "voucher": None,
        },
    )
    assert roles == [Role.SPEAKER, Role.ATTENDEE]


def test_get_roles_with_manual_user_id_override(requests_mock):
    conference = ConferenceFactory()

    attendee_user = UserFactory()
    AttendeeConferenceRole.objects.create(
        user_id=attendee_user.id, conference=conference, roles=[Role.SPEAKER.value]
    )

    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/vouchers",
        status_code=200,
        json={"next": None, "results": []},
    )

    roles = _get_roles(
        conference=conference,
        user_id=attendee_user.id,
        ticket={
            "id": 1,
            "voucher": None,
        },
    )
    assert roles == [Role.SPEAKER]


def test_get_roles_with_manual_user_id_when_they_have_no_ticket(requests_mock):
    conference = ConferenceFactory()

    attendee_user = UserFactory()
    AttendeeConferenceRole.objects.create(
        user_id=attendee_user.id, conference=conference, roles=[Role.SPEAKER.value]
    )

    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/vouchers",
        status_code=200,
        json={"next": None, "results": []},
    )

    roles = _get_roles(
        conference=conference,
        user_id=attendee_user.id,
        ticket=None,
    )
    assert roles == [Role.SPEAKER]


def test_get_roles_with_manual_order_position_id_override(requests_mock):
    conference = ConferenceFactory()

    AttendeeConferenceRole.objects.create(
        order_position_id=10, conference=conference, roles=[Role.KEYNOTER.value]
    )

    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/vouchers",
        status_code=200,
        json={"next": None, "results": []},
    )

    roles = _get_roles(
        conference=conference,
        user_id=UserFactory().id,
        ticket={
            "id": 10,
            "voucher": None,
        },
    )
    assert roles == [Role.KEYNOTER]


def test_get_roles_with_unrelated_override(requests_mock):
    conference = ConferenceFactory()

    AttendeeConferenceRole.objects.create(
        order_position_id=53, conference=conference, roles=[Role.KEYNOTER.value]
    )

    attendee_user = UserFactory()
    AttendeeConferenceRole.objects.create(
        user_id=attendee_user.id, conference=conference, roles=[Role.KEYNOTER.value]
    )

    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/vouchers",
        status_code=200,
        json={"next": None, "results": []},
    )

    roles = _get_roles(
        conference=conference,
        user_id=UserFactory().id,
        ticket={
            "id": 2000,
            "voucher": None,
        },
    )
    assert roles == [Role.ATTENDEE]


def test_get_conference_roles_for_user(requests_mock):
    conference = ConferenceFactory()
    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/vouchers",
        status_code=200,
        json={"next": None, "results": []},
    )

    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/tickets/attendee-tickets",
        status_code=200,
        json=[
            {
                "id": 1,
                "voucher": None,
                "attendee_email": "test@email.it",
                "item": {
                    "admission": True,
                },
            }
        ],
    )

    roles = get_conference_roles_for_user(
        conference=conference,
        user_id=UserFactory(email="test@email.it").id,
        user_email="test@email.it",
    )
    assert roles == [Role.ATTENDEE]


def test_get_conference_roles_for_user_as_sponsor(requests_mock):
    user = UserFactory()
    conference = ConferenceFactory()
    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/vouchers",
        status_code=200,
        json={
            "next": None,
            "results": [
                {
                    "id": 1,
                    "code": "12313123",
                    "tag": "sponsor,bit44",
                }
            ],
        },
    )

    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/tickets/attendee-tickets",
        status_code=200,
        json=[
            {
                "id": 1,
                "voucher": 1,
                "attendee_email": user.email,
                "item": {
                    "admission": True,
                },
            }
        ],
    )

    roles = get_conference_roles_for_user(
        conference=conference, user_id=user.id, user_email=user.email
    )

    assert roles == [Role.SPONSOR, Role.ATTENDEE]
