import pytest
from newsletters.exporter import convert_user_to_endpoint


@pytest.mark.django_db
def test_has_list_of_talks_per_conference(
    user_factory, conference, submission_factory, schedule_item_factory
):
    user = user_factory()

    submission = submission_factory(speaker=user, conference=conference)
    item = schedule_item_factory(
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
                f"{item.conference.code}_items_in_schedule": [item.title],
            },
        },
    }
