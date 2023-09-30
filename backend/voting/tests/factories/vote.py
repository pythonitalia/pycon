import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from submissions.tests.factories import SubmissionFactory
from voting.models import Vote


@register
class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote
        django_get_or_create = ("user_id", "submission")

    value = factory.fuzzy.FuzzyInteger(
        Vote.VALUES.not_interested, Vote.VALUES.must_see, 1
    )
    submission = factory.SubFactory(SubmissionFactory)
