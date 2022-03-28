import datetime

import pytest
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


def test_book_schedule_item(graphql_client, user, mocker, simple_schedule_item):
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=True)
    graphql_client.force_login(user)

    schedule_item = simple_schedule_item

    response = graphql_client.query(
        """mutation($id: ID!) {
        bookScheduleItem(id: $id) {
            __typename
            ... on ScheduleItem {
                spacesLeft
                userHasSpot
            }
        }
    }""",
        variables={"id": schedule_item.id},
    )

    assert response["data"]["bookScheduleItem"]["__typename"] == "ScheduleItem"
    assert response["data"]["bookScheduleItem"]["spacesLeft"] == 29
    assert response["data"]["bookScheduleItem"]["userHasSpot"] is True

    assert ScheduleItemAttendee.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()


def test_needs_ticket_to_book(
    graphql_client,
    user,
    simple_schedule_item,
    mocker,
):
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=False)

    graphql_client.force_login(user)

    schedule_item = simple_schedule_item

    response = graphql_client.query(
        """mutation($id: ID!) {
        bookScheduleItem(id: $id) {
            __typename
        }
    }""",
        variables={"id": schedule_item.id},
    )

    assert (
        response["data"]["bookScheduleItem"]["__typename"]
        == "UserNeedsConferenceTicket"
    )

    assert not ScheduleItemAttendee.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()


def test_cannot_overbook(
    graphql_client, user, simple_schedule_item, mocker, schedule_item_attendee_factory
):
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=True)

    graphql_client.force_login(user)

    schedule_item = simple_schedule_item
    schedule_item.attendees_total_capacity = 1
    schedule_item.save()

    schedule_item_attendee_factory(schedule_item=schedule_item, user_id=5000)

    response = graphql_client.query(
        """mutation($id: ID!) {
        bookScheduleItem(id: $id) {
            __typename
        }
    }""",
        variables={"id": schedule_item.id},
    )

    assert response["data"]["bookScheduleItem"]["__typename"] == "ScheduleItemIsFull"

    assert not ScheduleItemAttendee.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()


def test_user_cannot_book_twice(
    graphql_client, user, simple_schedule_item, mocker, schedule_item_attendee_factory
):
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=True)

    graphql_client.force_login(user)

    schedule_item = simple_schedule_item

    schedule_item_attendee_factory(schedule_item=schedule_item, user_id=user.id)

    response = graphql_client.query(
        """mutation($id: ID!) {
        bookScheduleItem(id: $id) {
            __typename
        }
    }""",
        variables={"id": schedule_item.id},
    )

    assert response["data"]["bookScheduleItem"]["__typename"] == "UserIsAlreadyBooked"

    assert ScheduleItemAttendee.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()


def test_user_cannot_book_any_event(
    graphql_client, user, simple_schedule_item, mocker, schedule_item_attendee_factory
):
    mocker.patch("api.schedule.mutations.user_has_admission_ticket", return_value=True)

    graphql_client.force_login(user)

    schedule_item = simple_schedule_item
    schedule_item.attendees_total_capacity = None
    schedule_item.save()

    response = graphql_client.query(
        """mutation($id: ID!) {
        bookScheduleItem(id: $id) {
            __typename
        }
    }""",
        variables={"id": schedule_item.id},
    )

    assert (
        response["data"]["bookScheduleItem"]["__typename"] == "ScheduleItemNotBookable"
    )

    assert not ScheduleItemAttendee.objects.filter(
        schedule_item=schedule_item, user_id=user.id
    ).exists()
