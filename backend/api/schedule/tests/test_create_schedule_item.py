from conferences.tests.factories import KeynoteFactory
from i18n.strings import LazyI18nString
from django.contrib.admin.models import LogEntry
from languages.models import Language
import pytest
from schedule.models import ScheduleItem as ScheduleItemModel
from submissions.tests.factories import SubmissionFactory

pytestmark = pytest.mark.django_db


def _create_schedule_item(client, **input):
    return client.query(
        """mutation CreateScheduleItem($input: CreateScheduleItemInput!) {
        createScheduleItem(input: $input) {
            id
            items {
                id
            }
        }
    }""",
        variables={
            "input": input,
        },
    )


@pytest.mark.parametrize("user_to_test", ["admin_user", "user", "not_authenticated"])
def test_cannot_create_schedule_item_with_no_permissions(
    admin_graphql_api_client,
    admin_user,
    user_to_test,
    user,
    conference_with_schedule_setup,
):
    if user_to_test == "admin_user":
        admin_graphql_api_client.force_login(admin_user)
    elif user_to_test == "user":
        admin_graphql_api_client.force_login(user)

    english_lang = Language.objects.get(code="en")

    conference = conference_with_schedule_setup
    submission = SubmissionFactory(
        conference=conference,
    )
    submission.languages.add(english_lang)

    day = conference.days.first()
    slot = day.slots.first()
    room = day.added_rooms.first().room

    response = _create_schedule_item(
        admin_graphql_api_client,
        conferenceId=conference.id,
        type=ScheduleItemModel.TYPES.talk,
        slotId=slot.id,
        rooms=[room.id],
        languageId=None,
        proposalId=submission.hashid,
    )

    assert response["errors"][0]["message"] == "Cannot edit schedule"
    assert not response.get("data")

    assert not ScheduleItemModel.objects.exists()
    assert not LogEntry.objects.exists()


def test_schedule_item_with_proposal(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    english_lang = Language.objects.get(code="en")

    conference = conference_with_schedule_setup
    submission = SubmissionFactory(
        conference=conference,
    )
    submission.languages.add(english_lang)

    day = conference.days.first()
    slot = day.slots.first()
    room = day.added_rooms.first().room

    response = _create_schedule_item(
        admin_graphql_api_client,
        conferenceId=conference.id,
        type=ScheduleItemModel.TYPES.talk,
        slotId=slot.id,
        rooms=[room.id],
        languageId=None,
        proposalId=submission.hashid,
    )

    assert not response.get("errors")

    schedule_item = ScheduleItemModel.objects.get()

    assert schedule_item.conference_id == conference.id
    assert schedule_item.type == ScheduleItemModel.TYPES.talk
    assert schedule_item.slot_id == slot.id
    assert schedule_item.submission_id == submission.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == room.id
    assert schedule_item.title == submission.title.localize("en")
    assert schedule_item.language_id == english_lang.id

    log_entry = LogEntry.objects.get()
    assert log_entry.object_id == str(schedule_item.id)
    assert log_entry.change_message == "Created Schedule Item"


def test_schedule_item_with_multi_lingual_proposal(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    italian_lang = Language.objects.get(code="it")

    admin_graphql_api_client.force_login(admin_superuser)

    conference = conference_with_schedule_setup
    submission = SubmissionFactory(
        conference=conference,
        title=LazyI18nString(
            {
                "it": "Italian title",
                "en": "English title",
            }
        ),
    )
    submission.languages.add(Language.objects.get(code="en"))
    submission.languages.add(italian_lang)

    day = conference.days.first()
    slot = day.slots.first()
    room = day.added_rooms.first().room

    response = _create_schedule_item(
        admin_graphql_api_client,
        conferenceId=conference.id,
        type=ScheduleItemModel.TYPES.talk,
        slotId=slot.id,
        rooms=[room.id],
        languageId=italian_lang.id,
        proposalId=submission.hashid,
    )

    assert not response.get("errors")

    schedule_item = ScheduleItemModel.objects.get()

    assert schedule_item.conference_id == conference.id
    assert schedule_item.type == ScheduleItemModel.TYPES.talk
    assert schedule_item.slot_id == slot.id
    assert schedule_item.submission_id == submission.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == room.id
    assert schedule_item.language_id == italian_lang.id
    assert schedule_item.title == "Italian title"


def test_schedule_item_with_keynote(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    english_lang = Language.objects.get(code="en")

    conference = conference_with_schedule_setup
    keynote = KeynoteFactory(
        conference=conference,
        title=LazyI18nString(
            {
                "it": "Italian title",
                "en": "English title",
            }
        ),
    )

    day = conference.days.first()
    slot = day.slots.first()
    room = day.added_rooms.first().room

    response = _create_schedule_item(
        admin_graphql_api_client,
        conferenceId=conference.id,
        type=ScheduleItemModel.TYPES.keynote,
        slotId=slot.id,
        rooms=[room.id],
        languageId=None,
        proposalId=None,
        keynoteId=keynote.id,
    )

    assert not response.get("errors")

    schedule_item = ScheduleItemModel.objects.get()

    assert schedule_item.conference_id == conference.id
    assert schedule_item.type == ScheduleItemModel.TYPES.keynote
    assert schedule_item.slot_id == slot.id
    assert schedule_item.submission_id is None
    assert schedule_item.keynote_id == keynote.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == room.id
    assert schedule_item.title == "English title"
    assert schedule_item.language_id == english_lang.id


def test_schedule_item_with_custom_item(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    english_lang = Language.objects.get(code="en")

    conference = conference_with_schedule_setup

    day = conference.days.first()
    slot = day.slots.first()
    rooms = day.added_rooms.values_list("id", flat=True)

    response = _create_schedule_item(
        admin_graphql_api_client,
        conferenceId=conference.id,
        type=ScheduleItemModel.TYPES.announcements,
        slotId=slot.id,
        rooms=list(rooms),
        languageId=None,
        proposalId=None,
        keynoteId=None,
        title="Announcements",
    )

    assert not response.get("errors")
    data = response["data"]

    schedule_item = ScheduleItemModel.objects.get()

    assert data["createScheduleItem"]["id"] == str(slot.id)
    assert data["createScheduleItem"]["items"] == [
        {"id": str(schedule_item.id)},
    ]

    assert schedule_item.conference_id == conference.id
    assert schedule_item.type == ScheduleItemModel.TYPES.announcements
    assert schedule_item.slot_id == slot.id
    assert schedule_item.submission_id is None
    assert schedule_item.keynote_id is None
    assert schedule_item.rooms.count() == 2
    assert set(schedule_item.rooms.values_list("id", flat=True)) == set(rooms)
    assert schedule_item.title == "Announcements"
    assert schedule_item.language_id == english_lang.id
