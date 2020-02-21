import pytest
from newsletters.exporter import convert_user_to_endpoint


@pytest.mark.django_db
def test_converts_one_user(user_factory):
    user = user_factory()

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == []
    assert endpoint.has_item_in_schedule == []
    assert endpoint.has_cancelled_talks == []
