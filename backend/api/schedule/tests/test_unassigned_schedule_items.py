from datetime import time
from i18n.strings import LazyI18nString
import pytest
from schedule.models import ScheduleItem
from schedule.tests.factories import ScheduleItemFactory, SlotFactory

pytestmark = pytest.mark.django_db


def _unassigned_schedule_items(client, **input):
    return client.query(
        """query UnassignedScheduleItems($conferenceId: ID!) {
        unassignedScheduleItems(conferenceId: $conferenceId) {
            id
        }
    }""",
        variables={**input},
    )


@pytest.mark.parametrize("user_to_test", ["admin_user", "user", "not_authenticated"])
def test_cannot_fetch_unassigned_schedule_items_with_no_permissions(
    admin_graphql_api_client,
    user_to_test,
    user,
    admin_user,
    conference_with_schedule_setup,
):
    if user_to_test == "admin_user":
        admin_graphql_api_client.force_login(admin_user)
    elif user_to_test == "user":
        admin_graphql_api_client.force_login(user)

    conference = conference_with_schedule_setup

    ScheduleItemFactory(
        conference=conference,
        submission=None,
        title=LazyI18nString({"en": "My TDD talk", "it": ""}),
        type=ScheduleItem.TYPES.talk,
        slot=None,
    )

    ScheduleItemFactory(
        conference=conference,
        submission=None,
        title=LazyI18nString({"en": "My TDD talk", "it": ""}),
        type=ScheduleItem.TYPES.talk,
        slot=SlotFactory(day__conference=conference, hour=time(9, 10), duration=30),
    )

    response = _unassigned_schedule_items(
        admin_graphql_api_client, conferenceId=conference.id
    )

    assert response["errors"][0]["message"] == "Cannot edit schedule"
    assert not response.get("data")


def test_fetch_unassigned_schedule_items(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    conference = conference_with_schedule_setup

    schedule_item_1 = ScheduleItemFactory(
        conference=conference,
        submission=None,
        title=LazyI18nString({"en": "My TDD talk", "it": ""}),
        type=ScheduleItem.TYPES.talk,
        slot=None,
    )

    ScheduleItemFactory(
        conference=conference,
        submission=None,
        title=LazyI18nString({"en": "My TDD talk", "it": ""}),
        type=ScheduleItem.TYPES.talk,
        slot=SlotFactory(day__conference=conference, hour=time(9, 10), duration=30),
    )

    response = _unassigned_schedule_items(
        admin_graphql_api_client, conferenceId=conference.id
    )

    assert response["data"]["unassignedScheduleItems"] == [
        {"id": str(schedule_item_1.id)},
    ]
