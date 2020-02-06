import random
from math import sqrt

import pytest
from voting.models import RankRequest, Vote


@pytest.fixture
def _setup_random(
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


# TODO: rename this fixture
@pytest.fixture
def _setup_equal(conference_factory, user_factory, submission_factory, vote_factory):
    conference = conference_factory()
    users = user_factory.create_batch(15)
    submissions = submission_factory.create_batch(5, conference=conference)

    vote_factory(user=users[0], submission=submissions[0], value=1)
    vote_factory(user=users[0], submission=submissions[1], value=2)
    vote_factory(user=users[0], submission=submissions[2], value=3)
    vote_factory(user=users[0], submission=submissions[3], value=4)

    vote_factory(user=users[1], submission=submissions[0], value=1)
    vote_factory(user=users[1], submission=submissions[1], value=2)
    vote_factory(user=users[1], submission=submissions[2], value=3)

    vote_factory(user=users[2], submission=submissions[0], value=1)
    vote_factory(user=users[2], submission=submissions[1], value=2)

    vote_factory(user=users[3], submission=submissions[0], value=1)

    vote_factory(user=users[5], submission=submissions[0], value=1)
    vote_factory(user=users[5], submission=submissions[1], value=2)
    vote_factory(user=users[5], submission=submissions[2], value=3)
    vote_factory(user=users[5], submission=submissions[3], value=4)

    vote_factory(user=users[6], submission=submissions[0], value=1)
    vote_factory(user=users[6], submission=submissions[1], value=2)
    vote_factory(user=users[6], submission=submissions[2], value=3)

    vote_factory(user=users[7], submission=submissions[0], value=1)
    vote_factory(user=users[7], submission=submissions[1], value=2)

    vote_factory(user=users[8], submission=submissions[0], value=1)

    vote_factory(user=users[10], submission=submissions[0], value=1)
    vote_factory(user=users[10], submission=submissions[1], value=2)
    vote_factory(user=users[10], submission=submissions[2], value=3)
    vote_factory(user=users[10], submission=submissions[3], value=4)

    vote_factory(user=users[11], submission=submissions[0], value=1)
    vote_factory(user=users[11], submission=submissions[1], value=2)
    vote_factory(user=users[11], submission=submissions[2], value=3)

    vote_factory(user=users[12], submission=submissions[0], value=1)
    vote_factory(user=users[12], submission=submissions[1], value=2)

    vote_factory(user=users[13], submission=submissions[0], value=1)

    users_weights = {
        users[0].pk: pytest.approx(sqrt(4)),
        users[1].pk: pytest.approx(sqrt(3)),
        users[2].pk: pytest.approx(sqrt(2)),
        users[3].pk: pytest.approx(sqrt(1)),
        users[5].pk: pytest.approx(sqrt(4)),
        users[6].pk: pytest.approx(sqrt(3)),
        users[7].pk: pytest.approx(sqrt(2)),
        users[8].pk: pytest.approx(sqrt(1)),
        users[10].pk: pytest.approx(sqrt(4)),
        users[11].pk: pytest.approx(sqrt(3)),
        users[12].pk: pytest.approx(sqrt(2)),
        users[13].pk: pytest.approx(sqrt(1)),
    }
    votes = Vote.objects.all()
    ranked_submissions = [
        {
            "submission_id": submissions[3].id,
            "submission__topic_id": submissions[3].topic.id,
            "score": 4.0,
        },
        {
            "submission_id": submissions[2].id,
            "submission__topic_id": submissions[2].topic.id,
            "score": 3.0000000000000004,
        },
        {
            "submission_id": submissions[1].id,
            "submission__topic_id": submissions[1].topic.id,
            "score": 2.0,
        },
        {
            "submission_id": submissions[0].id,
            "submission__topic_id": submissions[0].topic.id,
            "score": 1.0,
        },
        {
            "submission_id": submissions[4].id,
            "submission__topic_id": submissions[4].topic.id,
            "score": 0,
        },
    ]
    return conference, votes, users_weights, ranked_submissions


@pytest.mark.django_db
def test_most_voted_based_algorithm(_setup_equal):
    conference, votes, _, ranked_submissions = _setup_equal

    ranking = RankRequest.objects.create(conference=conference)
    for index, rank in enumerate(
        ranking.rank_submissions.all().order_by("absolute_rank")
    ):
        assert rank.submission.id == ranked_submissions[index]["submission_id"]
        assert round(rank.absolute_score, 2) == round(
            ranked_submissions[index]["score"], 2
        )


@pytest.mark.django_db
def test_weights(_setup_equal):
    _, votes, weights, _ = _setup_equal
    assert weights == RankRequest.get_users_weights(votes)
