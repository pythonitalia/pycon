import datetime

from schedule.tests.factories import DayFactory, ScheduleItemFactory, SlotFactory
from submissions.tests.factories import SubmissionFactory
import pytest

from schedule.models import ScheduleItem, ScheduleItemStar

pytestmark = pytest.mark.django_db


def test_get_starred_schedule_items(
    graphql_client,
    user,
):
    graphql_client.force_login(user)
    submission = SubmissionFactory()

    schedule_item = ScheduleItemFactory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=SlotFactory(
            day=DayFactory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )
    ScheduleItemStar.objects.create(schedule_item=schedule_item, user_id=user.id)

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                starredScheduleItems(conference: $conference)
            }
        }""",
        variables={"conference": submission.conference.code},
    )

    starred_schedule_items = response["data"]["me"]["starredScheduleItems"]
    assert list(starred_schedule_items) == [str(schedule_item.id)]
