import pytest

from voting.models import RankRequest, Vote

pytestmark = pytest.mark.django_db


@pytest.fixture
def _setup_simple_weigths(
    conference_factory, user_factory, submission_factory, vote_factory
):
    conference = conference_factory(topics=["Pizza", "Sushi"])
    sushi = conference.topics.get(name="Sushi")
    pizza = conference.topics.get(name="Pizza")
    submissions = []
    submissions.append(submission_factory(conference=conference, topic=sushi))
    submissions.append(submission_factory(conference=conference, topic=sushi))
    submissions.append(submission_factory(conference=conference, topic=sushi))
    submissions.append(submission_factory(conference=conference, topic=sushi))
    submissions.append(submission_factory(conference=conference, topic=pizza))
    submissions.append(submission_factory(conference=conference, topic=pizza))
    submissions.append(submission_factory(conference=conference, topic=pizza))

    user1 = user_factory()
    user2 = user_factory()

    vote_factory(user_id=user1.id, submission=submissions[0], value=1)
    vote_factory(user_id=user1.id, submission=submissions[1], value=2)
    vote_factory(user_id=user1.id, submission=submissions[2], value=3)
    vote_factory(user_id=user1.id, submission=submissions[3], value=4)

    vote_factory(user_id=user2.id, submission=submissions[0], value=1)
    vote_factory(user_id=user2.id, submission=submissions[6], value=4)

    users_weights = {
        (user1.id, sushi.id): 2.0,
        (user2.id, pizza.id): 1.0,
        (user2.id, sushi.id): 1.0,
    }
    votes = Vote.objects.all()

    ranked_submissions = [
        {
            "submission_id": submissions[3].id,
            "submission__topic_id": submissions[3].topic.id,
            "score": 4.0,
        },
        {
            "submission_id": submissions[6].id,
            "submission__topic_id": submissions[6].topic.id,
            "score": 4.0,
        },
        {
            "submission_id": submissions[2].id,
            "submission__topic_id": submissions[2].topic.id,
            "score": 3.0,
        },
        {
            "submission_id": submissions[5].id,
            "submission__topic_id": submissions[5].topic.id,
            "score": 0.0,
        },
        {
            "submission_id": submissions[4].id,
            "submission__topic_id": submissions[4].topic.id,
            "score": 0,
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
    ]
    return conference, votes, users_weights, ranked_submissions


@pytest.mark.django_db
def test_most_voted_based_algorithm(_setup_simple_weigths):
    conference, _, _, ranked_submissions = _setup_simple_weigths

    ranking = RankRequest.objects.create(conference=conference, is_public=True)
    for index, rank in enumerate(ranking.rank_submissions.all().order_by("rank")):
        assert rank.submission.id == ranked_submissions[index]["submission_id"]
        assert round(rank.score, 2) == round(ranked_submissions[index]["score"], 2)


def test_ranking_only_on_proposed_submissions(conference, submission_factory):
    valid_submission = submission_factory(status="proposed", conference=conference)
    cancelled_submission = submission_factory(status="cancelled", conference=conference)

    ranking = RankRequest.objects.create(conference=conference, is_public=True)

    submissions_ids = [rs.submission.pk for rs in ranking.rank_submissions.all()]
    assert len(submissions_ids) == 1
    assert valid_submission.pk in submissions_ids
    assert cancelled_submission.pk not in submissions_ids


def test_weights(_setup_simple_weigths):
    _, votes, weights, _ = _setup_simple_weigths
    assert weights == RankRequest.get_users_weights(votes)
