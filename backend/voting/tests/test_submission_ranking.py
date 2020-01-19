import random

import pytest
from voting.models import RankRequest


@pytest.fixture
def _setup(
    conference_factory, submission_factory, user_factory, vote_factory, random_vote
):
    conference = conference_factory()

    USERS_NUMBER = random.randint(10, 20)
    # only 5% of the users will make a proposal usually...
    SUBMISSION_NUMBER = int(USERS_NUMBER * 0.5)

    users = user_factory.create_batch(USERS_NUMBER)
    submissions = submission_factory.create_batch(
        SUBMISSION_NUMBER, conference=conference
    )

    counts_votes = {}
    for submission in submissions:
        counts_votes[submission.pk] = 0

    for user in users:
        for submission in submissions:
            # make more realistic: skip some voting...
            if bool(random.getrandbits(1)):
                continue

            value = random_vote()
            vote_factory(user=user, value=value, submission=submission)
            counts_votes[submission.pk] += value

    return conference, counts_votes


# TODO test most_voted_based
# @pytest.mark.django_db
# def test_votes_counts(_setup):
#     conference, votes_counts = _setup
#
#     ranked_submissions = RankRequest.users_most_voted_based(conference)
#     for rank in ranked_submissions:
#         assert votes_counts[rank["submission_id"]] == rank["score"]


@pytest.mark.django_db
def test_simple_sum_algorithm(_setup):
    conference, votes_counts = _setup

    ranked_submissions = RankRequest.simple_sum(conference)
    for rank in ranked_submissions:
        assert votes_counts[rank["submission_id"]] == rank["score"]


# @pytest.mark.django_db
# def test_create_ranking(_setup):
#     conference, votes_counts = _setup
#
#     rank_request = RankRequest.objects.create(conference=conference)
#
#     for rank in rank_request.rank_submissions.filter(rank_request=rank_request):
#         assert votes_counts[rank.submission.id] == rank.absolute_score
