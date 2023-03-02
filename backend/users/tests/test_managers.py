import datetime

import pytest
from users.managers import UserManager
from users.models import User


@pytest.mark.django_db
def test_create_user_empty_email():
    with pytest.raises(ValueError) as error:
        UserManager().create_user("", "johnpassword")

    assert "The given email must be set" in str(error.value)


@pytest.mark.django_db
def test_create_user_with_email_and_password():
    user = User.objects.create_user("lennon@thebeatles.com", "johnpassword")

    assert user.email == "lennon@thebeatles.com"
    assert not user.is_superuser
    assert not user.is_staff


@pytest.mark.django_db
def test_create_user_with_extra_fields():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        name="John",
        full_name="John Lennon",
        gender="male",
        date_birth=datetime.datetime.strptime("09/10/1940", "%d/%m/%Y"),
    )

    assert user.name == "John"
    assert user.full_name == "John Lennon"
    assert user.gender == "male"
    assert user.date_birth == datetime.datetime.strptime("09/10/1940", "%d/%m/%Y")


@pytest.mark.django_db
def test_create_user_superuser_with_email_and_password():
    user = User.objects.create_user(
        "lennon@thebeatles.com", "johnpassword", is_superuser=True
    )

    assert user.email == "lennon@thebeatles.com"
    assert user.is_superuser
    assert not user.is_staff


@pytest.mark.django_db
def test_cannot_create_superuser_not_superuser_flag():
    with pytest.raises(ValueError) as error:
        User.objects.create_superuser(
            "lennon@thebeatles.com", "johnpassword", is_superuser=False
        )

    assert "Superuser must have is_superuser=True." in str(error.value)


@pytest.mark.django_db
def test_create_superuser_with_email_and_password():
    user = User.objects.create_superuser("lennon@thebeatles.com", "johnpassword")

    assert user.email == "lennon@thebeatles.com"
    assert user.is_staff
    assert user.is_superuser
