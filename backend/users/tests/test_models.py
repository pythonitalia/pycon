import pytest
from django.contrib.auth import authenticate, get_user_model
from django.core import exceptions

from users.managers import UserManager
from users.models import User


def test_that_get_user_model_returns_correct_model():
    assert get_user_model() == User


@pytest.mark.django_db
def test_user_manager():
    assert isinstance(User.objects, UserManager)


@pytest.mark.django_db
def test_create_user_and_authenticate():
    user = User.objects.create_user("lennon@thebeatles.com", "johnpassword")

    authenticated_user = authenticate(
        username="lennon@thebeatles.com", password="johnpassword"
    )

    assert user == authenticated_user


@pytest.mark.django_db
def test_user_get_short_name():
    user = User.objects.create_user("lennon@thebeatles.com", "johnpassword")

    assert "lennon@thebeatles.com" == user.get_short_name()


@pytest.mark.django_db
def test_business_user_clean_missing_business_name():
    user = User.objects.create_user("lennon@thebeatles.com", "johnpassword")
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_company_fields()

    assert exc_info.type is exceptions.ValidationError
    assert list(exc_info.value.args[0].keys()) == ["business_name"]
    assert list(exc_info.value.args[0].values()) == [
        "Missing Business Name in your user profile."
    ]


@pytest.mark.django_db
def test_business_user_clean_missing_phone_number():
    user = User.objects.create_user(
        "lennon@thebeatles.com", "johnpassword", business_name="ACME, Inc."
    )
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_company_fields()

    assert exc_info.type is exceptions.ValidationError
    assert list(exc_info.value.args[0].keys()) == ["phone_number"]
    assert list(exc_info.value.args[0].values()) == [
        "Missing Phone Number in your user profile."
    ]


@pytest.mark.django_db
def test_business_user_clean_specify_vat_number_or_cf_code():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
    )
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_company_fields()

    assert exc_info.type is exceptions.ValidationError
    assert (
        "Please specify Fiscal Code or VAT number in your user profile."
        in exc_info.value
    )


@pytest.mark.django_db
def test_business_user_clean_country_it_and_not_pec_and_recipient_code():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
        country="IT",
        vat_number="IT01234567890",
        recipient_code="",
        pec_address="",
    )
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_company_fields()

    assert exc_info.type is exceptions.ValidationError
    assert (
        "For Italian companies for electronic invoicing it is mandatory "
        "to specify the recipient's code or the pec address." in exc_info.value
    )
