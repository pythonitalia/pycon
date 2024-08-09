from users.tests.factories import UserFactory
from conferences.tests.factories import ConferenceFactory
from schedule.tests.factories import ScheduleItemFactory
from submissions.tests.factories import SubmissionFactory
import pytest

from newsletters.exporter import convert_user_to_endpoint

pytestmark = pytest.mark.skip(reason="disabled export for now")


@pytest.mark.django_db
def test_convert_to_item():
    conference = ConferenceFactory()
    user = UserFactory()

    submission = SubmissionFactory(speaker_id=user.id, conference=conference)
    item = ScheduleItemFactory(
        type="submission", submission=submission, conference=conference
    )

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.to_item() == {
        "ChannelType": "EMAIL",
        "Address": endpoint.email,
        "Id": endpoint.id,
        "User": {
            "UserId": endpoint.id,
            "UserAttributes": {
                "Name": [endpoint.name],
                "FullName": [endpoint.full_name],
                "is_staff": [str(endpoint.is_staff)],
                "has_item_in_schedule": [item.conference.code],
                "has_cancelled_talks": [],
                "has_ticket": [],
                f"{item.conference.code}_items_in_schedule": [item.title],
            },
        },
    }
