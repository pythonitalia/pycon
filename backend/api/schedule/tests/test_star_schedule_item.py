import datetime

import pytest

from schedule.models import ScheduleItem, ScheduleItemStar

pytestmark = pytest.mark.django_db


def test_star_schedule_item(
    submission_factory,
    graphql_client,
    user,
    schedule_item_factory,
    slot_factory,
    day_factory,
):
    graphql_client.force_login(user)
    submission = submission_factory()

    schedule_item = schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )

    response = graphql_client.query(
        """mutation($id: ID!) {
        starScheduleItem(id: $id)
    }""",
        variables={"id": schedule_item.id},
    )

    assert not response.get("errors")
    assert ScheduleItemStar.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()


def test_unstar_schedule_item(
    submission_factory,
    graphql_client,
    user,
    schedule_item_factory,
    slot_factory,
    day_factory,
):
    graphql_client.force_login(user)
    submission = submission_factory()

    schedule_item = schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )

    ScheduleItemStar.objects.create(schedule_item=schedule_item, user_id=user.id)

    response = graphql_client.query(
        """mutation($id: ID!) {
        unstarScheduleItem(id: $id)
    }""",
        variables={"id": schedule_item.id},
    )

    assert not response.get("errors")
    assert not ScheduleItemStar.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()
