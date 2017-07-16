import pytest


@pytest.fixture()
def user():
    from users.models import User

    return User.objects.create_user(
        "user@test.com",
        "password"
    )
