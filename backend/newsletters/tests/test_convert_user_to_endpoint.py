import pytest

from newsletters.exporter import convert_user_to_endpoint

pytestmark = pytest.mark.skip(reason="disabled export for now")


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


@pytest.mark.django_db
def test_adds_submissions_sent(user_factory, conference, submission_factory):
    user = user_factory()

    submission_factory(speaker_id=user.id, conference=conference)

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == [conference.code]
    assert endpoint.has_item_in_schedule == []
    assert endpoint.has_cancelled_talks == []


@pytest.mark.django_db
def test_adds_items_in_schedule(
    user_factory, conference, submission_factory, schedule_item_factory
):
    user = user_factory()

    submission = submission_factory(speaker_id=user.id, conference=conference)
    schedule_item_factory(
        type="submission", submission=submission, conference=conference
    )

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == [conference.code]
    assert endpoint.has_item_in_schedule == [conference.code]
    assert endpoint.has_cancelled_talks == []


@pytest.mark.django_db
def test_adds_items_in_schedule_even_if_additional_speaker(
    user_factory,
    conference,
    submission_factory,
    schedule_item_factory,
    schedule_item_additional_speaker_factory,
):
    user = user_factory()
    additional_user = user_factory()

    submission = submission_factory(speaker_id=user.id, conference=conference)
    item = schedule_item_factory(
        type="submission", submission=submission, conference=conference
    )
    schedule_item_additional_speaker_factory(
        scheduleitem=item, user_id=additional_user.id
    )

    endpoint = convert_user_to_endpoint(additional_user)

    assert endpoint.id == str(additional_user.id)
    assert endpoint.name == additional_user.name
    assert endpoint.full_name == additional_user.full_name
    assert endpoint.is_staff == additional_user.is_staff
    assert endpoint.has_sent_submission_to == []
    assert endpoint.has_item_in_schedule == [conference.code]
    assert endpoint.has_cancelled_talks == []


@pytest.mark.django_db
def test_has_list_of_talks_per_conference(
    user_factory, conference, submission_factory, schedule_item_factory
):
    user = user_factory()

    submission = submission_factory(speaker_id=user.id, conference=conference)
    item = schedule_item_factory(
        type="submission", submission=submission, conference=conference
    )

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == [conference.code]
    assert endpoint.has_item_in_schedule == [conference.code]
    assert endpoint.has_cancelled_talks == []
    assert endpoint.talks_by_conference == {conference.code: [item.title]}


@pytest.mark.django_db
def test_adds_cancelled_talks(user_factory, conference, submission_factory):
    user = user_factory()

    submission_factory(speaker_id=user.id, conference=conference, status="cancelled")

    endpoint = convert_user_to_endpoint(user)

    assert endpoint.id == str(user.id)
    assert endpoint.name == user.name
    assert endpoint.full_name == user.full_name
    assert endpoint.is_staff == user.is_staff
    assert endpoint.has_sent_submission_to == [conference.code]
    assert endpoint.has_item_in_schedule == []
    assert endpoint.has_cancelled_talks == [conference.code]
