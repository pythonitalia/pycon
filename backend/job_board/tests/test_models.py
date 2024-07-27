from job_board.tests.factories import JobListingFactory
import pytest


pytestmark = pytest.mark.django_db


def test_automatic_slug():
    post = JobListingFactory(slug=None)
    assert post.slug
