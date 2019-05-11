from pytest import mark

from django.utils import timezone

from schedule.models import ScheduleItem


def _query_conference_schedule(client, conference_code, date=None):
    formatted_date = None

    if date:
        formatted_date = date.isoformat()

    return client.query(
        """
        query($code: String, $date: Date) {
            conference(code: $code) {
                schedule(date: $date) {
                    id
                    type
                    title
                    submission {
                        id
                    }
                }
            }
        }
    """,
        variables={"code": conference_code, "date": formatted_date},
    )


@mark.django_db
def test_query_conference_schedule(
    graphql_client, conference_factory, schedule_item_factory, submission_factory
):
    now = timezone.now()

    conference = conference_factory(start=now, end=now + timezone.timedelta(days=3))

    item1 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title="Welcome!",
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1),
    )

    test_submission = submission_factory(conference=conference)

    item2 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=test_submission,
        start=now + timezone.timedelta(hours=1),
        end=now + timezone.timedelta(hours=2),
    )

    resp = _query_conference_schedule(graphql_client, conference.code)

    assert len(resp["data"]["conference"]["schedule"]) == 2
    assert {
        "id": str(item1.id),
        "type": item1.type.upper(),
        "title": item1.title,
        "submission": None,
    } in resp["data"]["conference"]["schedule"]

    assert {
        "id": str(item2.id),
        "type": item2.type.upper(),
        "title": item2.title,
        "submission": {"id": str(item2.submission.id)},
    } in resp["data"]["conference"]["schedule"]


@mark.django_db
def test_schedule_is_ordered_by_start_date(
    graphql_client, conference_factory, schedule_item_factory, submission_factory
):
    now = timezone.now()

    conference = conference_factory(start=now, end=now + timezone.timedelta(days=3))

    item1 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title="Welcome!",
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1),
    )

    test_submission = submission_factory(conference=conference)

    item2 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=test_submission,
        start=now + timezone.timedelta(hours=1),
        end=now + timezone.timedelta(hours=2),
    )

    test_submission_2 = submission_factory(conference=conference)

    item3 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=test_submission_2,
        start=now + timezone.timedelta(minutes=30),
        end=now + timezone.timedelta(hours=1),
    )

    resp = _query_conference_schedule(graphql_client, conference.code)

    assert {
        "id": str(item1.id),
        "type": item1.type.upper(),
        "title": item1.title,
        "submission": None,
    } == resp["data"]["conference"]["schedule"][0]

    assert {
        "id": str(item3.id),
        "type": item3.type.upper(),
        "title": item3.title,
        "submission": {"id": str(item3.submission.id)},
    } == resp["data"]["conference"]["schedule"][1]

    assert {
        "id": str(item2.id),
        "type": item2.type.upper(),
        "title": item2.title,
        "submission": {"id": str(item2.submission.id)},
    } == resp["data"]["conference"]["schedule"][2]


@mark.django_db
def test_get_specific_day_schedule(
    graphql_client, conference_factory, schedule_item_factory, submission_factory
):
    now = timezone.now()

    conference = conference_factory(start=now, end=now + timezone.timedelta(days=3))

    day_item = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title="Welcome!",
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1),
    )

    tomorrow = now + timezone.timedelta(days=1)

    another_day_item = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=submission_factory(conference=conference),
        start=tomorrow,
        end=tomorrow + timezone.timedelta(hours=1),
    )

    resp = _query_conference_schedule(graphql_client, conference.code, date=now.date())

    assert len(resp["data"]["conference"]["schedule"]) == 1
    assert {
        "id": str(day_item.id),
        "type": day_item.type.upper(),
        "title": day_item.title,
        "submission": None,
    } in resp["data"]["conference"]["schedule"]

    assert {
        "id": str(another_day_item.id),
        "type": another_day_item.type.upper(),
        "title": another_day_item.title,
        "submission": {"id": str(another_day_item.submission.id)},
    } not in resp["data"]["conference"]["schedule"]


@mark.django_db
def test_get_scheduleitem_room(
    graphql_client,
    conference_factory,
    schedule_item_factory,
    submission_factory,
    room_factory,
):
    now = timezone.now()

    conference = conference_factory(start=now, end=now + timezone.timedelta(days=3))

    room = room_factory(conference=conference)
    room2 = room_factory(conference=conference)

    schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title="Welcome!",
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1),
        rooms=(room,),
    )

    tomorrow = now + timezone.timedelta(days=1)

    schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=submission_factory(conference=conference),
        start=tomorrow,
        end=tomorrow + timezone.timedelta(hours=1),
        rooms=(room2,),
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                schedule {
                    rooms {
                        name
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert len(resp["data"]["conference"]["schedule"]) == 2

    assert {"rooms": [{"name": room.name}]} in resp["data"]["conference"]["schedule"]

    assert {"rooms": [{"name": room2.name}]} in resp["data"]["conference"]["schedule"]


@mark.django_db
def test_get_additional_speakers(
    graphql_client,
    conference_factory,
    schedule_item_factory,
    submission_factory,
    room_factory,
    user_factory,
):
    another_speaker = user_factory()

    now = timezone.now()

    conference = conference_factory(start=now, end=now + timezone.timedelta(days=3))

    room = room_factory(conference=conference)

    schedule = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title="Welcome!",
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1),
        rooms=(room,),
    )

    schedule.additional_speakers.add(another_speaker)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                schedule {
                    additionalSpeakers {
                        id
                        username
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert resp["data"]["conference"]["schedule"] == [
        {
            "additionalSpeakers": [
                {"id": str(another_speaker.id), "username": another_speaker.username}
            ]
        }
    ]
