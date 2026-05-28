import datetime

from schedule.tests.factories import (
    DayFactory,
    ScheduleItemAttendeeFactory,
    ScheduleItemFactory,
    SlotFactory,
)
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory
import pytest

from schedule.models import ScheduleItem

pytestmark = pytest.mark.django_db


def _bookable_schedule_item(attendees_total_capacity: int = 30):
    submission = SubmissionFactory()
    return ScheduleItemFactory(
        status=ScheduleItem.STATUS.confirmed,
        submission=submission,
        type=ScheduleItem.TYPES.training,
        conference=submission.conference,
        attendees_total_capacity=attendees_total_capacity,
        slot=SlotFactory(
            day=DayFactory(
                day=datetime.date(2020, 10, 10),
                conference=submission.conference,
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )


def test_get_booked_schedule_items(graphql_client, user):
    graphql_client.force_login(user)

    booked_item = _bookable_schedule_item()
    _bookable_schedule_item()
    ScheduleItemAttendeeFactory(schedule_item=booked_item, user_id=user.id)

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                bookedScheduleItems(conference: $conference) {
                    id
                    title
                    slug
                    start
                    end
                }
            }
        }""",
        variables={"conference": booked_item.conference.code},
    )

    booked_schedule_items = response["data"]["me"]["bookedScheduleItems"]
    assert len(booked_schedule_items) == 1
    assert booked_schedule_items[0]["id"] == str(booked_item.id)
    assert booked_schedule_items[0]["slug"] == booked_item.slug
    assert booked_schedule_items[0]["start"] is not None
    assert booked_schedule_items[0]["end"] is not None


def test_booked_schedule_items_excludes_items_without_slot(graphql_client, user):
    graphql_client.force_login(user)

    submission = SubmissionFactory()
    unscheduled_workshop = ScheduleItemFactory(
        status=ScheduleItem.STATUS.confirmed,
        submission=submission,
        type=ScheduleItem.TYPES.training,
        conference=submission.conference,
        attendees_total_capacity=30,
        slot=None,
    )
    ScheduleItemAttendeeFactory(schedule_item=unscheduled_workshop, user_id=user.id)

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                bookedScheduleItems(conference: $conference) {
                    id
                    start
                    end
                }
            }
        }""",
        variables={"conference": unscheduled_workshop.conference.code},
    )

    assert response["data"]["me"]["bookedScheduleItems"] == []


def test_booked_schedule_items_excludes_other_users_bookings(graphql_client, user):
    graphql_client.force_login(user)

    booked_item = _bookable_schedule_item()
    other_user = UserFactory()
    ScheduleItemAttendeeFactory(schedule_item=booked_item, user_id=other_user.id)

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                bookedScheduleItems(conference: $conference) {
                    id
                }
            }
        }""",
        variables={"conference": booked_item.conference.code},
    )

    assert response["data"]["me"]["bookedScheduleItems"] == []


def test_booked_schedule_items_requires_authentication(graphql_client):
    schedule_item = _bookable_schedule_item()
    ScheduleItemAttendeeFactory(schedule_item=schedule_item)

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                bookedScheduleItems(conference: $conference) {
                    id
                }
            }
        }""",
        variables={"conference": schedule_item.conference.code},
    )

    assert response["errors"][0]["message"] == "User not logged in"
