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


@pytest.mark.django_db
def test_inactive_user_is_not_a_member(memberships):
    _, inactive, _ = memberships

    assert Membership.objects.is_member(inactive) == False


@pytest.mark.django_db
def test_active_user_is_a_member(memberships):
    active, _, _ = memberships

    assert Membership.objects.is_member(active) == True


@pytest.mark.django_db
def test_never_user_is_not_a_member(memberships):
    _, _, never = memberships

    assert Membership.objects.is_member(never) == False

@pytest.mark.django_db
def test_create_membership(user):
    member = Membership.objects.create_membership(user)

    assert member.user == user
    assert Membership.objects.is_member(user) == True
