from conferences.tests.factories import ConferenceFactory
from submissions.tests.factories import SubmissionFactory, SubmissionTagFactory
import pytest

from voting.models import RankRequest

pytestmark = pytest.mark.django_db


def test_tag_count_should_remain_the_same():
    conference = ConferenceFactory()
    pizza = SubmissionTagFactory(name="Pizza")
    sushi = SubmissionTagFactory(name="Sushi")
    polenta = SubmissionTagFactory(name="Polenta")

    SubmissionFactory(
        conference=conference,
        tags=["Polenta"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Polenta"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Pizza", "Sushi"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Pizza", "Sushi"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Pizza", "Polenta"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Pizza", "Polenta"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Polenta", "Sushi", "Sushi"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Pizza"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Pizza"],
    )
    SubmissionFactory(
        conference=conference,
        tags=["Polenta"],
    )

    ranking = RankRequest.objects.create(conference=conference, is_public=True)

    assert ranking.rank_submissions.filter(tag=polenta).count() == 6
    assert ranking.rank_submissions.filter(tag=sushi).count() == 3
    assert ranking.rank_submissions.filter(tag=pizza).count() == 6
