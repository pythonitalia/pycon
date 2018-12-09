from pytest import mark, raises

from datetime import datetime

from django.utils import timezone
from django.core import exceptions


@mark.django_db
def test_deadline_start_cannot_be_after_end(deadline_factory):
    deadline = deadline_factory(
        start=timezone.make_aware(datetime(2018, 5, 5)),
        end=timezone.make_aware(datetime(2018, 4, 4))
    )

    with raises(exceptions.ValidationError) as e:
        deadline.clean()

    assert 'Start date cannot be after end' in str(e.value)


@mark.django_db
def test_conference_cannot_have_two_deadlines_of_type_event(deadline_factory):
    deadline1 = deadline_factory(
        type='event',
        start=timezone.make_aware(datetime(2018, 5, 5)),
        end=timezone.make_aware(datetime(2018, 6, 3))
    )

    deadline1.clean()

    deadline2 = deadline_factory(
        type='event',
        conference=deadline1.conference,
        start=timezone.make_aware(datetime(2018, 6, 5)),
        end=timezone.make_aware(datetime(2018, 10, 4))
    )

    with raises(exceptions.ValidationError) as e:
        deadline2.clean()

    assert 'You can only have one deadline of type event' in str(e.value)


@mark.django_db
def test_conference_cannot_have_two_deadlines_of_type_cfp(deadline_factory):
    deadline1 = deadline_factory(
        type='cfp',
        start=timezone.make_aware(datetime(2018, 5, 5)),
        end=timezone.make_aware(datetime(2018, 6, 3))
    )

    deadline1.clean()

    deadline2 = deadline_factory(
        type='cfp',
        conference=deadline1.conference,
        start=timezone.make_aware(datetime(2018, 6, 5)),
        end=timezone.make_aware(datetime(2018, 10, 4))
    )

    with raises(exceptions.ValidationError) as e:
        deadline2.clean()

    assert 'You can only have one deadline of type cfp' in str(e.value)


@mark.django_db
def test_conference_cannot_have_two_deadlines_of_type_voting(deadline_factory):
    deadline1 = deadline_factory(
        type='voting',
        start=timezone.make_aware(datetime(2018, 5, 5)),
        end=timezone.make_aware(datetime(2018, 6, 3))
    )

    deadline1.clean()

    deadline2 = deadline_factory(
        type='voting',
        conference=deadline1.conference,
        start=timezone.make_aware(datetime(2018, 6, 5)),
        end=timezone.make_aware(datetime(2018, 10, 4))
    )

    with raises(exceptions.ValidationError) as e:
        deadline2.clean()

    assert 'You can only have one deadline of type voting' in str(e.value)


@mark.django_db
def test_conference_cannot_have_two_deadlines_of_type_refund(deadline_factory):
    deadline1 = deadline_factory(
        type='refund',
        start=timezone.make_aware(datetime(2018, 5, 5)),
        end=timezone.make_aware(datetime(2018, 6, 3))
    )

    deadline1.clean()

    deadline2 = deadline_factory(
        type='refund',
        conference=deadline1.conference,
        start=timezone.make_aware(datetime(2018, 6, 5)),
        end=timezone.make_aware(datetime(2018, 10, 4))
    )

    with raises(exceptions.ValidationError) as e:
        deadline2.clean()

    assert 'You can only have one deadline of type refund' in str(e.value)


@mark.django_db
def test_conference_can_have_multiple_custom_deadlines(deadline_factory):
    deadline1 = deadline_factory(
        type='custom',
        start=timezone.make_aware(datetime(2018, 5, 5)),
        end=timezone.make_aware(datetime(2018, 6, 3))
    )

    deadline1.clean()

    deadline2 = deadline_factory(
        type='custom',
        start=timezone.make_aware(datetime(2018, 5, 5)),
        end=timezone.make_aware(datetime(2018, 6, 3))
    )

    deadline2.clean()


@mark.django_db
def test_conference_to_str(conference_factory):
    assert 'Ciao Mondo <ep1>' == str(conference_factory(name='Ciao Mondo', code='ep1'))
