from pytest import mark

from i18n.strings import LazyI18nString


@mark.django_db
def test_slug_is_not_regenerated_when_changing_title(submission_factory):
    submission = submission_factory(title=LazyI18nString({"en": "hello", "it": "hell"}))
    assert submission.slug == "hello"

    submission.title = LazyI18nString({"en": "ciao", "it": "cia"})
    submission.save()

    submission.refresh_from_db()

    assert submission.slug == "hello"
