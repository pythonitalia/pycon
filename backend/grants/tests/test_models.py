from grants.tests.factories import GrantFactory
from conferences.tests.factories import ConferenceFactory
import pytest

from grants.models import AidCategory
from grants.models import GrantAllocation
from grants.tests.factories import (
    AidCategoryFactory,
    CountryAidAmountFactory,
    GrantAllocationFactory,
)

pytestmark = pytest.mark.django_db


def test_grant_with_default_aid_categories():
    # Create an AidCategory that should be included by default
    default_category = AidCategoryFactory(included_by_default=True)

    # Create a Grant
    grant = GrantFactory(conference=default_category.conference)

    # Ensure that the default AidCategory is included in the Grant's allocations
    assert GrantAllocation.objects.filter(
        grant=grant, category=default_category
    ).exists()


def test_grant_travel_aid_calculation():
    # Create a conference and country-specific travel cost
    conference = ConferenceFactory()
    country_aid = CountryAidAmountFactory(conference=conference, max_amount=300)

    # Create a travel-related AidCategory
    travel_category = AidCategoryFactory(
        conference=conference, category=AidCategory.AidType.TRAVEL
    )

    # Create a Grant with travelling_from matching the country aid
    grant = GrantFactory(
        conference=conference,
        travelling_from=country_aid.country,
        needs_funds_for_travel=True,
    )

    # Trigger save to assign aid categories
    grant.save()

    # Check that the travel allocation is correctly calculated
    travel_allocation = GrantAllocation.objects.get(
        grant=grant, category=travel_category
    )
    assert travel_allocation.allocated_amount == country_aid.max_amount


def test_grant_with_custom_allocated_amount():
    # Create a custom AidCategory
    custom_category = AidCategoryFactory(max_amount=400)

    # Create a Grant and manually allocate a custom amount
    grant = GrantFactory()
    allocation = GrantAllocationFactory(
        grant=grant, category=custom_category, allocated_amount=350
    )

    # Ensure that the allocation is correct
    assert allocation.allocated_amount == 350
    assert allocation.category == custom_category
    assert allocation.grant == grant


@pytest.mark.django_db
def test_grant_has_approved_travel_true():
    travel_category = AidCategoryFactory(category=AidCategory.AidType.TRAVEL)
    grant = GrantFactory()
    GrantAllocationFactory(grant=grant, category=travel_category)

    # Test that has_approved_travel returns True
    assert grant.has_approved_travel() is True


@pytest.mark.django_db
def test_grant_has_approved_travel_false():
    grant = GrantFactory()

    assert grant.has_approved_travel() is False


@pytest.mark.django_db
def test_grant_has_approved_accommodation_true():
    accommodation_category = AidCategoryFactory(
        category=AidCategory.AidType.ACCOMMODATION
    )
    grant = GrantFactory()
    GrantAllocationFactory(grant=grant, category=accommodation_category)

    assert grant.has_approved_accommodation() is True


@pytest.mark.django_db
def test_grant_has_approved_accommodation_false():
    grant = GrantFactory()

    assert grant.has_approved_accommodation() is False
