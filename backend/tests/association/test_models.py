import pytest
import datetime
from freezegun import freeze_time

from association.models import Membership


@pytest.mark.django_db
def test_datetime_membership(user):
    with freeze_time("2017-01-01"):
        membership = Membership.objects.create(
            user=user
        )

    assert membership.date == datetime.datetime(2017, 1, 1)
