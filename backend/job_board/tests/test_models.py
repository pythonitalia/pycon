import pytest


@pytest.mark.django_db
def test_automatic_slug(job_listing_factory):
    post = job_listing_factory(slug=None)
    assert post.slug
