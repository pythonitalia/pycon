import pytest

from i18n.strings import LazyI18nString
from voting.admin import RankSubmissionResource
from voting.models import RankSubmission
from voting.tests.factories.ranking import RankSubmissionFactory

pytestmark = pytest.mark.django_db


def test_rank_submission_export_includes_submission_title():
    RankSubmissionFactory(submission__title=LazyI18nString({"en": "My talk"}))

    dataset = RankSubmissionResource().export(queryset=RankSubmission.objects.all())

    assert dataset.dict[0]["submission__title"] == "My talk"
