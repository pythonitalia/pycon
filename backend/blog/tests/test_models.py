from blog.tests.factories import PostFactory
import pytest


@pytest.mark.django_db
def test_automatic_slug():
    post = PostFactory(slug=None)
    assert post.slug
