from pytest import mark

from django.utils import timezone

from schedule.models import ScheduleItem


def _query_conference_schedule(client, conference_code, date=None, topic=None):
    formatted_date = None

    if date:
        formatted_date = date.strftime('%d/%m/%Y')

    return client.query("""
        query($code: String, $date: String, $topic: ID) {
            conference(code: $code) {
                schedule(date: $date, topic: $topic) {
                    id
                    type
                    title
                    submission {
                        id
                    }
                }
            }
        }
    """, variables={
        'code': conference_code,
        'date': formatted_date,
        'topic': topic
    })


@mark.django_db
def test_query_conference_schedule(
    graphql_client,
    conference_factory,
    schedule_item_factory,
    submission_factory
):
    now = timezone.now()

    conference = conference_factory(
        start=now,
        end=now + timezone.timedelta(days=3)
    )

    item1 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title='Welcome!',
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1)
    )

    test_submission = submission_factory(conference=conference)

    item2 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=test_submission,
        start=now + timezone.timedelta(hours=1),
        end=now + timezone.timedelta(hours=2)
    )

    resp = _query_conference_schedule(graphql_client, conference.code)

    assert len(resp['data']['conference']['schedule']) == 2
    assert {
        'id': str(item1.id),
        'type': item1.type.upper(),
        'title': item1.title,
        'submission': None
    } in resp['data']['conference']['schedule']

    assert {
        'id': str(item2.id),
        'type': item2.type.upper(),
        'title': item2.title,
        'submission': {
            'id': str(item2.submission.id),
        }
    } in resp['data']['conference']['schedule']


@mark.django_db
def test_schedule_is_ordered_by_start_date(
    graphql_client,
    conference_factory,
    schedule_item_factory,
    submission_factory
):
    now = timezone.now()

    conference = conference_factory(
        start=now,
        end=now + timezone.timedelta(days=3)
    )

    item1 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title='Welcome!',
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1)
    )

    test_submission = submission_factory(conference=conference)

    item2 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=test_submission,
        start=now + timezone.timedelta(hours=1),
        end=now + timezone.timedelta(hours=2)
    )

    test_submission_2 = submission_factory(conference=conference)

    item3 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=test_submission_2,
        start=now + timezone.timedelta(minutes=30),
        end=now + timezone.timedelta(hours=1)
    )

    resp = _query_conference_schedule(graphql_client, conference.code)

    assert {
        'id': str(item1.id),
        'type': item1.type.upper(),
        'title': item1.title,
        'submission': None
    } == resp['data']['conference']['schedule'][0]

    assert {
        'id': str(item3.id),
        'type': item3.type.upper(),
        'title': item3.title,
        'submission': {
            'id': str(item3.submission.id),
        }
    } == resp['data']['conference']['schedule'][1]

    assert {
        'id': str(item2.id),
        'type': item2.type.upper(),
        'title': item2.title,
        'submission': {
            'id': str(item2.submission.id),
        }
    } == resp['data']['conference']['schedule'][2]


@mark.django_db
def test_get_specific_day_schedule(
    graphql_client,
    conference_factory,
    schedule_item_factory,
    submission_factory
):
    now = timezone.now()

    conference = conference_factory(
        start=now,
        end=now + timezone.timedelta(days=3)
    )

    day_item = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title='Welcome!',
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1)
    )

    tomorrow = now + timezone.timedelta(days=1)

    another_day_item = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=submission_factory(conference=conference),
        start=tomorrow,
        end=tomorrow + timezone.timedelta(hours=1)
    )

    resp = _query_conference_schedule(graphql_client, conference.code, date=now.date())

    assert len(resp['data']['conference']['schedule']) == 1
    assert {
        'id': str(day_item.id),
        'type': day_item.type.upper(),
        'title': day_item.title,
        'submission': None
    } in resp['data']['conference']['schedule']

    assert {
        'id': str(another_day_item.id),
        'type': another_day_item.type.upper(),
        'title': another_day_item.title,
        'submission': {
            'id': str(another_day_item.submission.id),
        }
    } not in resp['data']['conference']['schedule']


@mark.django_db
def test_specific_topic_schedule(
    graphql_client,
    conference_factory,
    schedule_item_factory,
    submission_factory
):
    now = timezone.now()

    conference = conference_factory(
        start=now,
        end=now + timezone.timedelta(days=3)
    )

    item1 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.custom,
        title='Welcome!',
        submission=None,
        start=now,
        end=now + timezone.timedelta(hours=1)
    )

    test_submission = submission_factory(conference=conference)

    item2 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=test_submission,
        topic=item1.topic,
        start=now + timezone.timedelta(days=1, hours=1),
        end=now + timezone.timedelta(days=1, hours=2)
    )

    test_submission_2 = submission_factory(conference=conference)

    item3 = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.submission,
        submission=test_submission_2,
        start=now + timezone.timedelta(hours=1),
        end=now + timezone.timedelta(hours=2)
    )

    resp = _query_conference_schedule(graphql_client, conference.code, topic=item1.topic.id)

    assert len(resp['data']['conference']['schedule']) == 2

    assert {
        'id': str(item1.id),
        'type': item1.type.upper(),
        'title': item1.title,
        'submission': None
    } in resp['data']['conference']['schedule']

    assert {
        'id': str(item2.id),
        'type': item2.type.upper(),
        'title': item2.title,
        'submission': {
            'id': str(item2.submission.id),
        }
    } in resp['data']['conference']['schedule']

    assert {
        'id': str(item3.id),
        'type': item3.type.upper(),
        'title': item3.title,
        'submission': {
            'id': str(item3.submission.id),
        }
    } not in resp['data']['conference']['schedule']
