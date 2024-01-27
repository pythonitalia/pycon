import pytest
from api.cms.utils import get_site_by_host
from wagtail_factories import SiteFactory


pytestmark = pytest.mark.django_db


def test_hostname_no_port():
    site_1 = SiteFactory(hostname="localhost", port=80)
    SiteFactory(hostname="localhost", port=81)
    SiteFactory(hostname="example.org", port=80)

    selected_site = get_site_by_host("localhost")

    assert selected_site.id == site_1.id


def test_hostname_with_port():
    SiteFactory(hostname="localhost", port=80)
    site_2 = SiteFactory(hostname="localhost", port=81)
    SiteFactory(hostname="example.org", port=80)

    selected_site = get_site_by_host("localhost:81")

    assert selected_site.id == site_2.id


def test_hostname_with_no_matching_site():
    SiteFactory(hostname="localhost", port=80)
    SiteFactory(hostname="localhost", port=81)
    SiteFactory(hostname="example.org", port=80)

    selected_site = get_site_by_host("localhost:443")

    assert selected_site.id is None

    selected_site = get_site_by_host("example.org:120")

    assert selected_site.id is None
