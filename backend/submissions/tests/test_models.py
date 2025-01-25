from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory
from pytest import mark

from i18n.strings import LazyI18nString

pytestmark = mark.django_db


def test_slug_is_not_regenerated_when_changing_title():
    submission = SubmissionFactory(title=LazyI18nString({"en": "hello", "it": "hell"}))
    assert submission.slug == "hello"

    submission.title = LazyI18nString({"en": "ciao", "it": "cia"})
    submission.save()

    submission.refresh_from_db()

    assert submission.slug == "hello"


def test_syncs_pending_status_when_changing_status():
    submission = SubmissionFactory(
        status=Submission.STATUS.accepted,
        pending_status=Submission.STATUS.accepted,
    )

    submission.status = Submission.STATUS.rejected
    submission.save()

    submission.refresh_from_db()

    assert submission.status == Submission.STATUS.rejected
    assert submission.pending_status == Submission.STATUS.rejected


def test_leaves_pending_status_unchanged_if_different():
    submission = SubmissionFactory(
        status=Submission.STATUS.proposed,
        pending_status=Submission.STATUS.rejected,
    )

    submission.status = Submission.STATUS.waiting_list
    submission.save()

    submission.refresh_from_db()

    assert submission.status == Submission.STATUS.waiting_list
    assert submission.pending_status == Submission.STATUS.rejected
