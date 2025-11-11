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

    submission.slug = ""
    submission.save(update_fields=["title"])

    submission.refresh_from_db()

    assert submission.slug == "ciao"


def test_current_or_pending_status_returns_pending_if_set():
    submission = SubmissionFactory(
        status=Submission.STATUS.proposed,
        pending_status=Submission.STATUS.accepted,
    )

    assert submission.current_or_pending_status == Submission.STATUS.accepted


def test_current_or_pending_status_returns_current_if_pending_none():
    submission = SubmissionFactory(
        status=Submission.STATUS.rejected,
        pending_status=None,
    )

    assert submission.current_or_pending_status == Submission.STATUS.rejected


def test_pending_status_not_automatically_synced():
    submission = SubmissionFactory(
        status=Submission.STATUS.proposed,
        pending_status=Submission.STATUS.accepted,
    )

    submission.status = Submission.STATUS.rejected
    submission.save(update_fields=["status"])

    submission.refresh_from_db()

    assert submission.status == Submission.STATUS.rejected
    assert submission.pending_status == Submission.STATUS.accepted  # Should remain unchanged
