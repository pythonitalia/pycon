import random

import pytest
from submissions.models import Submission
from voting.models import RankRequest


@pytest.fixture
def _setup(
    conference_factory, submission_factory, user_factory, vote_factory, random_vote
):
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
    ranked_submissions = RankRequest.get_ranking(submissions)
    for rank in ranked_submissions:
        assert votes_counts[rank["submission_id"]] == rank["votes"]


@pytest.mark.django_db
def test_create_ranking(_setup):
    conference, votes_counts = _setup

    rank_request = RankRequest.objects.create(conference=conference)

    for rank in rank_request.rank_submissions.filter(rank_request=rank_request):
        assert votes_counts[rank.submission.id] == rank.absolute_score
