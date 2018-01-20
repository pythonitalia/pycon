import pytest

from django.contrib.admin.sites import AdminSite

from association.admin import MembershipAdmin
from association.models import Membership
from association.filters import YearFilter


@pytest.mark.django_db
def test_filter_lookup(memberships):
    admin = MembershipAdmin(Membership, AdminSite())
    filter = YearFilter({}, {}, Membership, admin)
    years = filter.lookups({}, admin)

    assert years == [(2018, 2018), (2016, 2016)]


@pytest.mark.django_db
def test_filter_queryset(memberships):
    admin = MembershipAdmin(Membership, AdminSite())
    filter = YearFilter({}, {'year': '2018'}, Membership, admin)
    filtered_queryset = filter.queryset({}, Membership.objects.all())

    queryset = Membership.objects.filter(date__year=2018)

    assert list(filtered_queryset) == list(queryset)

@pytest.mark.django_db
def test_filter_empty_queryset(memberships):
    admin = MembershipAdmin(Membership, AdminSite())
    filter = YearFilter({}, {}, Membership, admin)
    queryset = Membership.objects.all()
    filtered_queryset = filter.queryset({}, queryset)

    assert filtered_queryset == None
