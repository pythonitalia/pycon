import pytest


@pytest.mark.django_db
def test_automatic_slug(page_factory):
    page = page_factory(slug=None)
    assert page.slug
