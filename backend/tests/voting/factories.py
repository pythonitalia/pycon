import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from tests.conferences.factories import ConferenceFactory
from tests.submissions.factories import SubmissionFactory
from tests.users.factories import UserFactory
from voting.models import VoteRange, Vote


@register
class VoteRangeFactory(DjangoModelFactory):

    class Meta:
        model = VoteRange
        django_get_or_create = ('name', )


@register
class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    conference = factory.SubFactory(ConferenceFactory)
    range = factory.SubFactory(VoteRangeFactory)
    value = factory.fuzzy.FuzzyFloat(range.first, range.last) #?
    submission = factory.SubFactory(SubmissionFactory)
    user = factory.SubFactory(UserFactory)
