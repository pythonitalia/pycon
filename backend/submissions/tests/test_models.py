from pytest import mark


@mark.django_db
def test_slug_is_not_regenerated_when_changing_title(submission_factory):
    submission = submission_factory(title="hello")
    assert submission.slug == "hello"

    submission.title = "ciao"
    submission.save()

    submission.refresh_from_db()

    assert submission.slug == "hello"
