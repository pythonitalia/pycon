import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory
from voting.models import Vote


@register
class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    value = factory.fuzzy.FuzzyInteger(
        Vote.VALUES.not_interested, Vote.VALUES.must_see, 1
    )
    submission = factory.SubFactory(SubmissionFactory)
    user = factory.SubFactory(UserFactory)
