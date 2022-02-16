import random

import factory
import pytz
from factory import post_generation
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from submissions.tests.factories import SubmissionFactory
from voting.models import RankRequest, RankSubmission


@register
class RankRequestFactory(factory.django.DjangoModelFactory):

    conference = factory.SubFactory(ConferenceFactory)
    created = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    is_public = True

    class Meta:
        model = RankRequest

    @post_generation
    def rank_submissions(self, create, extracted):

        if not create:
            return

        if extracted:
            for rank_submission in extracted:
                self.rank_submissions.add(rank_submission)

    @post_generation
    def submissions(self, create, extracted):
        if not create:
            return

        if extracted:
            for submission in extracted:
                rank_submission = RankSubmissionFactory.create(submission=submission)
                self.rank_submissions.add(rank_submission)


@register
class RankSubmissionFactory(factory.django.DjangoModelFactory):

    rank_request = factory.SubFactory(RankRequestFactory)
    submission = factory.SubFactory(SubmissionFactory)

    rank = factory.Sequence(lambda n: n + 1)
    score = factory.Sequence(lambda n: (n + 1) * random.randint(n, 100))

    class Meta:
        model = RankSubmission
