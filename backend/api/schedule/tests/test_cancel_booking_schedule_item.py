import datetime

import pytest
import time_machine
from pytest import mark

from schedule.models import ScheduleItem, ScheduleItemAttendee

pytestmark = mark.django_db


@pytest.fixture
def simple_schedule_item(
    schedule_item_factory, submission_factory, slot_factory, day_factory
):
    submission = submission_factory(
        speaker_id=200,
    )

    return schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        attendees_total_capacity=30,
        slot=slot_factory(
            day=day_factory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )


def test_cancel_booking(
    graphql_client, user, simple_schedule_item, mocker, schedule_item_attendee_factory
):
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=True)

    graphql_client.force_login(user)

    schedule_item = simple_schedule_item

    schedule_item_attendee_factory(schedule_item=schedule_item, user_id=user.id)

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
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=True)

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
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=True)

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


def test_cancelling_a_booking_gives_the_space_to_the_next_person_in_waiting_list(
    graphql_client, user, simple_schedule_item, mocker, schedule_item_attendee_factory
):
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=True)

    graphql_client.force_login(user)

    schedule_item = simple_schedule_item

    with time_machine.travel("2022-10-10 10:00:00", tick=False):
        schedule_item_attendee_factory(schedule_item=schedule_item, user_id=user.id)

    with time_machine.travel("2022-10-10 11:00:00", tick=False):
        waiting_list_item = schedule_item_attendee_factory(
            schedule_item=schedule_item, user_id=6000, is_in_waiting_list=True
        )

    with time_machine.travel("2022-10-10 12:00:00", tick=False):
        second_waiting_in_list = schedule_item_attendee_factory(
            schedule_item=schedule_item, user_id=7000, is_in_waiting_list=True
        )

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
    assert response["data"]["cancelBookingScheduleItem"]["spacesLeft"] == 29
    assert response["data"]["cancelBookingScheduleItem"]["hasSpacesLeft"] is True

    assert not ScheduleItemAttendee.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()

    waiting_list_item.refresh_from_db()
    second_waiting_in_list.refresh_from_db()

    assert not waiting_list_item.is_in_waiting_list
    assert second_waiting_in_list.is_in_waiting_list
