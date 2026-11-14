import pytest
from django.contrib import admin

from i18n.strings import LazyI18nString
from voting.admin import RankSubmissionResource, VoteAdmin
from voting.models import RankSubmission, Vote
from voting.tests.factories.ranking import RankSubmissionFactory
from voting.tests.factories.vote import VoteFactory

pytestmark = pytest.mark.django_db


def test_vote_changelist_filters_by_submission(rf, admin_superuser):
    vote = VoteFactory()
    VoteFactory()
    request = rf.get("/", {"submission__id__exact": vote.submission_id})
    request.user = admin_superuser

    changelist = VoteAdmin(Vote, admin.site).get_changelist_instance(request)

    assert list(changelist.queryset) == [vote]


def test_rank_submission_export_includes_submission_title():
    RankSubmissionFactory(submission__title=LazyI18nString({"en": "My talk"}))

    dataset = RankSubmissionResource().export(queryset=RankSubmission.objects.all())

    assert dataset.dict[0]["submission__title"] == "My talk"
