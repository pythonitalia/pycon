import random

import factory
import pytz
from conferences.tests.factories import ConferenceFactory
from factory import post_generation
from pytest_factoryboy import register
from submissions.tests.factories import SubmissionFactory
from voting.models import RankRequest, RankSubmission


@register
class RankRequestFactory(factory.DjangoModelFactory):

    conference = factory.SubFactory(ConferenceFactory)
    created = factory.Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = RankRequest

    @post_generation
    def rank_submissions(self, create, extracted):

        if not create:
            return

        if extracted:
            for rank_submission in extracted:
                self.rank_submissions.add(rank_submission)


@register
class RankSubmissionFactory(factory.DjangoModelFactory):

    rank_request = factory.SubFactory(RankRequestFactory)
    submission = factory.SubFactory(SubmissionFactory)

    absolute_rank = factory.Sequence(lambda n: n + 1)
    absolute_score = factory.Sequence(lambda n: (n + 1) * random.randint(n, 100))
    topic_rank = factory.Sequence(lambda n: n + 1)

    class Meta:
        model = RankSubmission
