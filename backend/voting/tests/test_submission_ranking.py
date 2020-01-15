import math
import random

import pytest
from django.core.management import CommandError, call_command
from voting.models import Vote


def random_vote():
    return math.floor(random.uniform(Vote.VALUES.not_interested, Vote.VALUES.must_see))


@pytest.fixture
def setup_case(conference_factory, submission_factory, user_factory, vote_factory):
    conference = conference_factory()
    submissions = submission_factory.create_batch(5, conference=conference)
    users = user_factory.create_batch(5)

    for submission in submissions:

        for user in users:
            # make more realistic: skip some voting...
            if bool(random.getrandbits(1)):
                continue
            value = random_vote()
            vote_factory(user=user, value=value, submission=submission)

    return conference


@pytest.mark.django_db
def test_submission_ranking(setup_case):
    conference = setup_case

    call_command("submisson_ranking", conference.code)

    assert True


def test_conference_not_provided():

    with pytest.raises(CommandError) as e:
        call_command("submisson_ranking")

    assert e.value.args[0] == "Error: the following arguments are required: conference"


@pytest.mark.django_db
def test_conference_does_not_exists(conference_factory):
    conference = conference_factory.build()

    with pytest.raises(CommandError) as e:
        call_command("submisson_ranking", conference.code)

    assert e.value.args[0] == f'Conference "{conference.code}" does not exist'
