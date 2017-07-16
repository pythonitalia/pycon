import pytest

from freezegun import freeze_time


@pytest.fixture()
def memberships():
    from users.models import User
    from association.models import Membership

    active = User.objects.create_user(
        "active@test.com",
        "password"
    )

    Membership.objects.create(
        user=active
    )

    with freeze_time("2016-01-01"):
        inactive = User.objects.create_user(
            "inactive@test.com",
            "password"
        )

        Membership.objects.create(
            user=inactive
        )

        never = User.objects.create_user(
            "never@test.com",
            "password"
        )

    return active, inactive, never
