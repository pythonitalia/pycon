from pytest import mark, raises

from datetime import datetime

from django.utils import timezone
from django.core import exceptions


@mark.django_db
def test_validation_does_not_fail_if_both_conference_start_and_end_are_not_specified(conference_factory):
    conference = conference_factory(end=None, start=None)
    conference.clean()


@mark.django_db
def test_validation_fails_without_both_conferencestart_and_end(conference_factory):
    conference = conference_factory(start=None)

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Please specify both start and end for Conference' in str(e.value)

    conference = conference_factory(end=None)

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Please specify both start and end for Conference' in str(e.value)


@mark.django_db
def test_conference_start_cannot_be_after_end(conference_factory):
    conference = conference_factory(
        start=timezone.make_aware(datetime(2018, 5, 5)),
        end=timezone.make_aware(datetime(2018, 4, 4))
    )

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Conference start date cannot be after end' in str(e.value)


@mark.django_db
def test_cfp_start_cannot_be_after_end(conference_factory):
    conference = conference_factory(
        cfp_start=timezone.make_aware(datetime(2018, 5, 5)),
        cfp_end=timezone.make_aware(datetime(2018, 4, 4))
    )

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'CFP start date cannot be after end' in str(e.value)


@mark.django_db
def test_refund_start_cannot_be_after_end(conference_factory):
    conference = conference_factory(
        refund_start=timezone.make_aware(datetime(2018, 5, 5)),
        refund_end=timezone.make_aware(datetime(2018, 4, 4))
    )

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Refund start date cannot be after end' in str(e.value)


@mark.django_db
def test_voting_start_cannot_be_after_end(conference_factory):
    conference = conference_factory(
        voting_start=timezone.make_aware(datetime(2018, 5, 5)),
        voting_end=timezone.make_aware(datetime(2018, 4, 4))
    )

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Voting start date cannot be after end' in str(e.value)


@mark.django_db
def test_validation_fails_without_both_cfpstart_end(conference_factory):
    conference = conference_factory(cfp_start=None)

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Please specify both start and end for CFP' in str(e.value)

    conference = conference_factory(cfp_end=None)

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Please specify both start and end for CFP' in str(e.value)


@mark.django_db
def test_validation_fails_without_both_votingstart_end(conference_factory):
    conference = conference_factory(voting_start=None)

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Please specify both start and end for Voting' in str(e.value)

    conference = conference_factory(voting_end=None)

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Please specify both start and end for Voting' in str(e.value)


@mark.django_db
def test_validation_fails_without_both_refundstart_end(conference_factory):
    conference = conference_factory(refund_start=None)

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Please specify both start and end for Refund' in str(e.value)

    conference = conference_factory(refund_end=None)

    with raises(exceptions.ValidationError) as e:
        conference.clean()

    assert 'Please specify both start and end for Refund' in str(e.value)


@mark.django_db
def test_validation_ignores_empty_conference_dates(conference_factory):
    conference = conference_factory(start=None, end=None)
    conference.clean()


@mark.django_db
def test_validation_ignores_empty_refund_dates(conference_factory):
    conference = conference_factory(refund_start=None, refund_end=None)
    conference.clean()


@mark.django_db
def test_validation_ignores_empty_cfp_dates(conference_factory):
    conference = conference_factory(cfp_start=None, cfp_end=None)
    conference.clean()


@mark.django_db
def test_validation_ignores_empty_voting_dates(conference_factory):
    conference = conference_factory(voting_start=None, voting_end=None)
    conference.clean()


@mark.django_db
def test_conference_to_str(conference_factory):
    assert 'Ciao Mondo <ep1>' == str(conference_factory(name='Ciao Mondo', code='ep1'))
