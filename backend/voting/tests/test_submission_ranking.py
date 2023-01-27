import pytest

from voting.models import RankRequest

pytestmark = pytest.mark.django_db


def test_tag_count_should_remain_the_same(
    submission_factory,
    submission_tag_factory,
    conference,
):
    pizza = submission_tag_factory(name="Pizza")
    sushi = submission_tag_factory(name="Sushi")
    polenta = submission_tag_factory(name="Polenta")

    submission_factory(
        conference=conference,
        tags=["Polenta"],
    )
    submission_factory(
        conference=conference,
        tags=["Polenta"],
    )
    submission_factory(
        conference=conference,
        tags=["Pizza", "Sushi"],
    )
    submission_factory(
        conference=conference,
        tags=["Pizza", "Sushi"],
    )
    submission_factory(
        conference=conference,
        tags=["Pizza", "Polenta"],
    )
    submission_factory(
        conference=conference,
        tags=["Pizza", "Polenta"],
    )
    submission_factory(
        conference=conference,
        tags=["Polenta", "Sushi", "Sushi"],
    )
    submission_factory(
        conference=conference,
        tags=["Pizza"],
    )
    submission_factory(
        conference=conference,
        tags=["Pizza"],
    )
    submission_factory(
        conference=conference,
        tags=["Polenta"],
    )

    ranking = RankRequest.objects.create(conference=conference, is_public=True)

    assert ranking.rank_submissions.filter(tag=polenta).count() == 6
    assert ranking.rank_submissions.filter(tag=sushi).count() == 3
    assert ranking.rank_submissions.filter(tag=pizza).count() == 6
