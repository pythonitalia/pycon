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
def test_create_user_with_extra_fields(country):
    country_uk = country("GB")
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        first_name="John",
        last_name="Lennon",
        gender="male",
        date_birth=datetime.datetime.strptime("09/10/1940", "%d/%m/%Y"),
        business_name="John Lennon Ltd",
        fiscal_code="LNNJHN40R09D037I",
        vat_number="IT01234567890",
        phone_number="+393381234567",
        recipient_code="XXXXXXX",
        pec_address="lennon@pec.it",
        address="42 Wallaby Way, Sydney",
        country=country_uk,
    )

    assert user.first_name == "John"
    assert user.last_name == "Lennon"
    assert user.gender == "male"
    assert user.date_birth == datetime.datetime.strptime("09/10/1940", "%d/%m/%Y")
    assert user.business_name == "John Lennon Ltd"
    assert user.fiscal_code == "LNNJHN40R09D037I"
    assert user.vat_number == "IT01234567890"
    assert user.phone_number == "+393381234567"
    assert user.recipient_code == "XXXXXXX"
    assert user.pec_address == "lennon@pec.it"
    assert user.address == "42 Wallaby Way, Sydney"
    assert user.country == country_uk


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
