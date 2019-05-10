import pytest

from pytest import mark

from django.core import exceptions

from schedule.models import ScheduleItem


@mark.django_db
def test_submission_is_required_if_type_is_submission(schedule_item_factory):
    schedule_item = schedule_item_factory(type=ScheduleItem.TYPES.submission, submission=None, title='')

    with pytest.raises(exceptions.ValidationError) as e:
        schedule_item.clean()

    assert 'You have to specify a submission when using the type `submission`' in str(e.value)


@mark.django_db
def test_title_cannot_be_blank_if_type_is_custom(schedule_item_factory):
    schedule_item = schedule_item_factory(type=ScheduleItem.TYPES.custom, title='')

    with pytest.raises(exceptions.ValidationError) as e:
        schedule_item.clean()

    assert 'You have to specify a title when using the type `custom`' in str(e.value)


@mark.django_db
def test_custom_item_with_title_is_correct(schedule_item_factory):
    schedule_item = schedule_item_factory(type=ScheduleItem.TYPES.custom, title='Hello')
    schedule_item.clean()
