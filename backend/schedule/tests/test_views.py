import pytz
from datetime import date, datetime, time, timezone
import icalendar
from conferences.tests.factories import ConferenceFactory
from django.urls import reverse
from pycon.signing import sign_path
import pytest
from schedule.models import ScheduleItem, ScheduleItemStar
from schedule.tests.factories import RoomFactory, ScheduleItemFactory, SlotFactory
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_user_schedule_item_favourites_calendar(client):
    user = UserFactory()
    conference = ConferenceFactory(timezone=pytz.timezone("Europe/Rome"))
    second_conf = ConferenceFactory()

    schedule_item_1 = ScheduleItemFactory(
        conference=conference,
        title="Starred Schedule Item",
        description="Description",
        submission=None,
        type=ScheduleItem.TYPES.talk,
        slot=SlotFactory(
            hour=time(10, 0),
            duration=30,
            day__day=date(2023, 1, 1),
            day__conference=conference,
        ),
    )
    schedule_item_1.rooms.add(RoomFactory(name="Room Name"))

    ScheduleItemFactory(
        conference=conference,
        title="Not starred",
        submission=None,
        type=ScheduleItem.TYPES.talk,
    )

    ScheduleItemFactory(
        conference=ConferenceFactory(),
        title="Another conf",
        submission=None,
        type=ScheduleItem.TYPES.talk,
    )

    ScheduleItemStar.objects.create(user=user, schedule_item=schedule_item_1)

    ScheduleItemStar.objects.create(user=UserFactory(), schedule_item=schedule_item_1)

    ScheduleItemStar.objects.create(
        user=UserFactory(),
        schedule_item=ScheduleItemFactory(
            conference=conference,
            title="Starred Schedule Item 2",
            description="Description 2",
            submission=None,
            type=ScheduleItem.TYPES.talk,
            slot=SlotFactory(
                hour=time(10, 0),
                duration=30,
                day__day=date(2023, 1, 1),
                day__conference=conference,
            ),
        ),
    )

    ScheduleItemStar.objects.create(
        user=user,
        schedule_item=ScheduleItemFactory(
            conference=second_conf,
            title="Starred Schedule Item 2",
            description="Description 2",
            submission=None,
            type=ScheduleItem.TYPES.talk,
            slot=SlotFactory(
                hour=time(10, 0),
                duration=30,
                day__day=date(2023, 1, 1),
                day__conference=second_conf,
            ),
        ),
    )

    path = reverse(
        "user-schedule-favourites-calendar",
        kwargs={"conference_id": conference.id, "hash_user_id": user.user_hashid()},
    )
    signed_path = sign_path(path)

    response = client.get(signed_path)

    assert response.headers["content-type"] == "text/calendar"
    assert (
        response.headers["Content-Disposition"] == 'attachment; filename="calendar.ics"'
    )

    calendar = icalendar.Calendar.from_ical(response.content)
    assert (
        calendar.get("x-wr-calname") == f"{conference.name.localize('en')}'s Schedule"
    )

    assert len(calendar.subcomponents) == 1

    event = calendar.subcomponents[0]
    assert (
        event.get("summary")
        == f"[{conference.name.localize('en')}] {schedule_item_1.title}"
    )
    assert event.get("location") == "Room Name"
    assert (
        event.get("description")
        == f"""Description

Room(s)/Stanza(/e): Room Name

Info: https://2024.pycon.it/event/{schedule_item_1.slug}/
""".strip()
    )
    assert event.get("dtstart").dt == datetime(2023, 1, 1, 9, 0, tzinfo=timezone.utc)
    assert event.get("dtend").dt == datetime(2023, 1, 1, 9, 30, tzinfo=timezone.utc)


def test_cannot_get_user_schedule_item_favourites_calendar_without_signature(client):
    conference = ConferenceFactory()
    user = UserFactory()

    path = reverse(
        "user-schedule-favourites-calendar",
        kwargs={"conference_id": conference.id, "hash_user_id": user.user_hashid()},
    )
    response = client.get(path)

    assert response.status_code == 403


def test_cannot_get_user_schedule_item_favourites_calendar_with_invalid_signature(
    client,
):
    conference = ConferenceFactory()
    user = UserFactory()

    path = reverse(
        "user-schedule-favourites-calendar",
        kwargs={"conference_id": conference.id, "hash_user_id": user.user_hashid()},
    )
    response = client.get(f"{path}?sh=123")

    assert response.status_code == 403


def test_cannot_get_user_schedule_item_favourites_calendar_with_other_user_signature(
    client,
):
    conference = ConferenceFactory()
    user = UserFactory()

    path = reverse(
        "user-schedule-favourites-calendar",
        kwargs={"conference_id": conference.id, "hash_user_id": user.user_hashid()},
    )
    other_path = reverse(
        "user-schedule-favourites-calendar",
        kwargs={
            "conference_id": conference.id,
            "hash_user_id": UserFactory().user_hashid(),
        },
    )

    signed_path = sign_path(path)
    signature = signed_path.split("=")[-1]

    response = client.get(f"{other_path}?sh={signature}")

    assert response.status_code == 403
