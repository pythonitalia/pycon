import pytest
import datetime
from freezegun import freeze_time

from association.models import Membership
from association.managers import MembershipManager


def test_model_manager():
    assert isinstance(Membership.objects, MembershipManager)


@pytest.mark.django_db
def test_datetime_membership(user):
    with freeze_time("2017-01-01"):
        membership = Membership.objects.create(
            user=user
        )

    assert membership.date == datetime.datetime(2017, 1, 1)
