from django.core import exceptions
from pytest import fail, mark, raises


@mark.django_db
def test_clean_validation(vote_range_factory):
    vote_range = vote_range_factory(first=1, last=10)
    vote_range.clean()


@mark.django_db
def test_range_first_cannot_be_greater_than_last(vote_range_factory):
    vote_range = vote_range_factory(first=10, last=1)

    with raises(exceptions.ValidationError) as e:
        vote_range.clean()

    assert "First vote cannot be greater then the last" in str(e.value)


@mark.django_db
def test_vote_must_be_beetween_first_and_last_range(vote_factory):
    vote = vote_factory(value=11)
    with raises(exceptions.ValidationError) as e:
        vote.clean()

    assert (
        f"Vote must be a value between {vote.submission.conference.vote_range.first} "
        f"and {vote.submission.conference.vote_range.last}" in (str(e.value))
    )


@mark.django_db
def test_vote_limits(vote_factory, vote_range_factory):
    vote_range = vote_range_factory()

    vote_minimum = vote_factory(value=vote_range.first)

    try:
        vote_minimum.clean()
    except exceptions.ValidationError as e:
        fail(f"Vote minimum Validator failed: {e}")

    vote_maximum = vote_factory(value=vote_range.last)

    try:
        vote_maximum.clean()
    except exceptions.ValidationError as e:
        fail(f"Vote maximum Validator failed: {e}")
