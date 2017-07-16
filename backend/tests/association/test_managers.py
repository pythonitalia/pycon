import pytest
import datetime
from freezegun import freeze_time

from association.models import Membership
from association.managers import MembershipManager


@pytest.mark.django_db
def test_inactive_members_empty():
    not_members = Membership.objects.inactives()

    assert not_members.count() == 0


@pytest.mark.django_db
def test_inactive_members(memberships):
    active, inactive, never = memberships
    not_members = Membership.objects.inactives()

    assert not_members.count() == 2
    assert active not in not_members
    assert inactive in not_members
    assert never in not_members


@pytest.mark.django_db
def test_inactive_members_of_a_year(memberships):
    active, inactive, never = memberships
    not_members = Membership.objects.inactives(year=2016)

    assert not_members.count() == 1
    assert active not in not_members
    assert inactive not in not_members
    assert never in not_members
