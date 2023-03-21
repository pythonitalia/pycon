import pytest
import respx
from django.conf import settings

from custom_auth.backend import UsersAuthBackend
from django.contrib.auth import get_user_model


pytestmark = pytest.mark.django_db


def test_authenticate():
    User = get_user_model()
    unrelated_user = User.objects.create(
        first_name="Hello", email="anotheremail@test.it"
    )

    backend = UsersAuthBackend()

    with respx.mock as mock:
        mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "login": {
                        "id": 1,
                        "email": "marco@test.it",
                        "fullname": "Test user",
                    }
                }
            }
        )

        logged_user = backend.authenticate(
            request=None, username="marco@test.it", password="hello"
        )

    assert logged_user.id != unrelated_user.id
    assert logged_user.email == "marco@test.it"
    assert logged_user.username == "marco@test.it"
    assert logged_user.first_name == "Test user"
    assert logged_user.is_staff
    assert not logged_user.is_superuser


def test_authenticate_when_wrong_username_or_password():
    backend = UsersAuthBackend()

    with respx.mock as mock:
        mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={"data": {"login": None}}
        )

        logged_user = backend.authenticate(
            request=None, username="marco@test.it", password="hello"
        )

    assert logged_user is None


def test_authenticate_with_existing_user():
    User = get_user_model()

    existing_user = User.objects.create(first_name="Hello", email="marco@test.it")
    backend = UsersAuthBackend()

    with respx.mock as mock:
        mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "login": {
                        "id": 1,
                        "email": "marco@test.it",
                        "fullname": "Test user",
                    }
                }
            }
        )

        logged_user = backend.authenticate(
            request=None, username="marco@test.it", password="hello"
        )

    assert logged_user.id == existing_user.id
    assert logged_user.first_name == "Test user"


def test_authenticate_with_validation_error():
    backend = UsersAuthBackend()

    with respx.mock as mock:
        mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={"errors": [{"message": "Invalid data"}]}
        )

        logged_user = backend.authenticate(
            request=None, username="marco", password="hello"
        )

    assert logged_user is None


def test_get_user():
    User = get_user_model()

    backend = UsersAuthBackend()
    user = User.objects.create(first_name="Hello", email="anotheremail@test.it")

    assert backend.get_user(user.id).id == user.id


def test_not_existent_user():
    User = get_user_model()

    backend = UsersAuthBackend()
    User.objects.create(id=1, first_name="Hello", email="anotheremail@test.it")

    assert backend.get_user(5000) is None
