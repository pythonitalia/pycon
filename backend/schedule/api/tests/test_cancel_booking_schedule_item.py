import datetime

from schedule.tests.factories import (
    DayFactory,
    ScheduleItemAttendeeFactory,
    ScheduleItemFactory,
    SlotFactory,
)
from submissions.tests.factories import SubmissionFactory
import pytest
from pytest import mark

from schedule.models import ScheduleItem, ScheduleItemAttendee

pytestmark = mark.django_db


@pytest.fixture
def simple_schedule_item():
    submission = SubmissionFactory()

    return ScheduleItemFactory(
        status=ScheduleItem.STATUS.confirmed,
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        attendees_total_capacity=30,
        slot=SlotFactory(
            day=DayFactory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )


def test_cancel_booking(
    graphql_client,
    user,
    simple_schedule_item,
):
    graphql_client.force_login(user)

    schedule_item = simple_schedule_item

    ScheduleItemAttendeeFactory(schedule_item=schedule_item, user_id=user.id)

    response = graphql_client.query(
        """mutation($id: ID!) {
        cancelBookingScheduleItem(id: $id) {
            __typename
            ... on ScheduleItem {
                userHasSpot
                hasSpacesLeft
                spacesLeft
            }
        }
    }""",
        variables={"id": schedule_item.id},
    )

    assert response["data"]["cancelBookingScheduleItem"]["__typename"] == "ScheduleItem"
    assert response["data"]["cancelBookingScheduleItem"]["userHasSpot"] is False
    assert response["data"]["cancelBookingScheduleItem"]["spacesLeft"] == 30
    assert response["data"]["cancelBookingScheduleItem"]["hasSpacesLeft"] is True

    assert not ScheduleItemAttendee.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()


def test_user_cannot_cancel_if_they_are_not_booked(
    graphql_client,
    user,
    simple_schedule_item,
    mocker,
):
    graphql_client.force_login(user)

    schedule_item = simple_schedule_item

    response = graphql_client.query(
        """mutation($id: ID!) {
        cancelBookingScheduleItem(id: $id) {
            __typename
        }
    }""",
        variables={"id": schedule_item.id},
    )

    assert (
        response["data"]["cancelBookingScheduleItem"]["__typename"] == "UserIsNotBooked"
    )


def test_cannot_cancel_if_schedule_item_is_not_bookable(
    graphql_client,
    user,
    simple_schedule_item,
    mocker,
):
    graphql_client.force_login(user)

    schedule_item = simple_schedule_item
    schedule_item.attendees_total_capacity = None
    schedule_item.save()

    response = graphql_client.query(
        """mutation($id: ID!) {
        cancelBookingScheduleItem(id: $id) {
            __typename
        }
    }""",
        variables={"id": schedule_item.id},
    )

    assert (
        response["data"]["cancelBookingScheduleItem"]["__typename"]
        == "ScheduleItemNotBookable"
    )
