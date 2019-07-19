import pytest
from blog.models import Post

@pytest.mark.django_db
def test_automatic_slug(post_factory):
    post = post_factory(slug=None)
    assert post.slug
