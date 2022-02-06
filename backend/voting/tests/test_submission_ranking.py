import random
from math import sqrt

import pytest

from voting.models import RankRequest, Vote

pytestmark = pytest.mark.django_db


@pytest.fixture
def _setup_random(
    conference_factory, submission_factory, user_factory, vote_factory, random_vote
):
    conference = conference_factory()

    USERS_NUMBER = random.randint(10, 20)
    # only 5% of the users will make a proposal usually...
    SUBMISSION_NUMBER = int(USERS_NUMBER * 0.5)

    users = [user_factory() for _ in range(USERS_NUMBER)]
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
            vote_factory(user_id=user.id, value=value, submission=submission)
            counts_votes[submission.pk] += value

    return conference, counts_votes


# TODO: rename this fixture
@pytest.fixture
def _setup_equal(conference_factory, user_factory, submission_factory, vote_factory):
    conference = conference_factory()

    users = [user_factory() for _ in range(15)]
    submissions = submission_factory.create_batch(5, conference=conference)

    vote_factory(user_id=users[0].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[0].id, submission=submissions[1], value=2)
    vote_factory(user_id=users[0].id, submission=submissions[2], value=3)
    vote_factory(user_id=users[0].id, submission=submissions[3], value=4)

    vote_factory(user_id=users[1].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[1].id, submission=submissions[1], value=2)
    vote_factory(user_id=users[1].id, submission=submissions[2], value=3)

    vote_factory(user_id=users[2].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[2].id, submission=submissions[1], value=2)

    vote_factory(user_id=users[3].id, submission=submissions[0], value=1)

    vote_factory(user_id=users[5].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[5].id, submission=submissions[1], value=2)
    vote_factory(user_id=users[5].id, submission=submissions[2], value=3)
    vote_factory(user_id=users[5].id, submission=submissions[3], value=4)

    vote_factory(user_id=users[6].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[6].id, submission=submissions[1], value=2)
    vote_factory(user_id=users[6].id, submission=submissions[2], value=3)

    vote_factory(user_id=users[7].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[7].id, submission=submissions[1], value=2)

    vote_factory(user_id=users[8].id, submission=submissions[0], value=1)

    vote_factory(user_id=users[10].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[10].id, submission=submissions[1], value=2)
    vote_factory(user_id=users[10].id, submission=submissions[2], value=3)
    vote_factory(user_id=users[10].id, submission=submissions[3], value=4)

    vote_factory(user_id=users[11].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[11].id, submission=submissions[1], value=2)
    vote_factory(user_id=users[11].id, submission=submissions[2], value=3)

    vote_factory(user_id=users[12].id, submission=submissions[0], value=1)
    vote_factory(user_id=users[12].id, submission=submissions[1], value=2)

    vote_factory(user_id=users[13].id, submission=submissions[0], value=1)

    users_weights = {
        users[0].id: pytest.approx(sqrt(4)),
        users[1].id: pytest.approx(sqrt(3)),
        users[2].id: pytest.approx(sqrt(2)),
        users[3].id: pytest.approx(sqrt(1)),
        users[5].id: pytest.approx(sqrt(4)),
        users[6].id: pytest.approx(sqrt(3)),
        users[7].id: pytest.approx(sqrt(2)),
        users[8].id: pytest.approx(sqrt(1)),
        users[10].id: pytest.approx(sqrt(4)),
        users[11].id: pytest.approx(sqrt(3)),
        users[12].id: pytest.approx(sqrt(2)),
        users[13].id: pytest.approx(sqrt(1)),
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


def test_ranking_only_on_proposed_submissions(conference, submission_factory):
    valid_submission = submission_factory(status="proposed", conference=conference)
    cancelled_submission = submission_factory(status="cancelled", conference=conference)

    ranking = RankRequest.objects.create(conference=conference)

    submissions_ids = [rs.submission.pk for rs in ranking.rank_submissions.all()]
    assert len(submissions_ids) == 1
    assert valid_submission.pk in submissions_ids
    assert cancelled_submission.pk not in submissions_ids


@pytest.mark.django_db
def test_weights(_setup_equal):
    _, votes, weights, _ = _setup_equal
    assert weights == RankRequest.get_users_weights(votes)
