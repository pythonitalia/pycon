import math
import random

import pytest
from django.core.management import CommandError, call_command
from submissions.models import Submission
from voting.management.commands.submisson_ranking import Command
from voting.models import Vote


def random_vote():
    return math.floor(random.uniform(Vote.VALUES.not_interested, Vote.VALUES.must_see))


@pytest.fixture
def _setup(conference_factory, submission_factory, user_factory, vote_factory):
    conference = conference_factory()

    SUBMISSION_NUMBER = random.randint(1, 10)
    USERS_NUMBER = random.randint(5, 20)
    submissions = submission_factory.create_batch(
        SUBMISSION_NUMBER, conference=conference
    )
    users = user_factory.create_batch(USERS_NUMBER)

    counts_votes = {}
    for submission in submissions:
        counts_votes[submission.pk] = 0
        for user in users:
            # make more realistic: skip some voting...
            if bool(random.getrandbits(1)):
                continue

            value = random_vote()
            vote_factory(user=user, value=value, submission=submission)
            counts_votes[submission.pk] += value

    return conference, counts_votes


@pytest.mark.django_db
def test_votes_counts(_setup):
    conference, votes_counts = _setup

    submissions = Submission.objects.filter(conference_id=conference.id)
    cmd = Command()
    ranked_submissions = cmd.rank_submissions(submissions)
    assert ranked_submissions
    for rank in ranked_submissions:
        assert votes_counts[rank["submission_id"]] == rank["votes"]


@pytest.mark.django_db
def test_submission_ranking(_setup):
    conference, _ = _setup

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
