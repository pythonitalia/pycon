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
def test_clean_business_fields_missing_business_name():
    user = User.objects.create_user("lennon@thebeatles.com", "johnpassword")
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_business_fields()

    assert exc_info.type is exceptions.ValidationError
    assert list(exc_info.value.args[0].keys()) == ["business_name"]
    assert list(exc_info.value.args[0].values()) == [
        "Missing Business Name in your user profile."
    ]


@pytest.mark.django_db
def test_clean_business_fields_missing_phone_number():
    user = User.objects.create_user(
        "lennon@thebeatles.com", "johnpassword", business_name="ACME, Inc."
    )
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_business_fields()

    assert exc_info.type is exceptions.ValidationError
    assert list(exc_info.value.args[0].keys()) == ["phone_number"]
    assert list(exc_info.value.args[0].values()) == [
        "Missing Phone Number in your user profile."
    ]


@pytest.mark.django_db
def test_clean_business_fields_missing_country():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
    )
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_business_fields()

    assert exc_info.type is exceptions.ValidationError
    assert list(exc_info.value.args[0].keys()) == ["country"]
    assert list(exc_info.value.args[0].values()) == [
        "Missing Country in your user profile."
    ]


@pytest.mark.django_db
def test_clean_business_fields_non_ue_country():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
        country="US",
    )
    assert user.clean_business_fields() is None


@pytest.mark.django_db
def test_clean_business_fields_ue_country_missing_vat():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
        country="FR",
    )
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_business_fields()

    assert exc_info.type is exceptions.ValidationError
    assert list(exc_info.value.args[0].keys()) == ["vat_number"]
    assert list(exc_info.value.args[0].values()) == [
        "Missing VAT Number in your user profile."
    ]


@pytest.mark.django_db
def test_clean_business_fields_ue_country_vat_ok():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
        vat_number="FR01234567890",
        country="FR",
    )
    assert user.clean_business_fields() is None


@pytest.mark.django_db
def test_clean_business_fields_it_ok():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
        vat_number="IT01234567890",
        recipient_code="XXXXXXX",
        country="IT",
    )
    assert user.clean_business_fields() is None


@pytest.mark.django_db
def test_clean_business_fields_it_ok_fiscal_code():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
        fiscal_code="NGRDTH62A48H313R",
        recipient_code="XXXXXXX",
        country="IT",
    )
    assert user.clean_business_fields() is None


@pytest.mark.django_db
def test_clean_business_fields_it_country_not_vat_number_cf_code_neither():
    user = User.objects.create_user(
        "lennon@thebeatles.com",
        "johnpassword",
        business_name="ACME, Inc.",
        phone_number="+39 3381234567",
        country="IT",
        vat_number="",
        fiscal_code="",
    )
    with pytest.raises(exceptions.ValidationError) as exc_info:
        user.clean_business_fields()

    assert exc_info.type is exceptions.ValidationError
    assert exc_info.type is exceptions.ValidationError
    assert (
        "Please specify Fiscal Code or VAT number in your user profile."
        in exc_info.value
    )


@pytest.mark.django_db
def test_clean_business_fields_country_it_not_pec_and_not_recipient_code():
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
        user.clean_business_fields()

    assert exc_info.type is exceptions.ValidationError
    assert (
        "For Italian companies for electronic invoicing it is mandatory "
        "to specify the recipient's code or the pec address." in exc_info.value
    )


@pytest.mark.django_db
def test_swiss_not_in_ue():
    user = User.objects.create_user(
        "lennon@thebeatles.com", "johnpassword", country="CH"
    )

    assert not user.is_eu()


@pytest.mark.django_db
def test_italy_in_ue():

    user = User.objects.create_user(
        "lennon@thebeatles.com", "johnpassword", country="IT"
    )

    assert user.is_eu()


@pytest.mark.django_db
def test_it_is_italian():
    user = User.objects.create_user(
        "lennon@thebeatles.com", "johnpassword", country="IT"
    )

    assert user.is_italian()


@pytest.mark.django_db
def test_non_italian():
    user = User.objects.create_user(
        "lennon@thebeatles.com", "johnpassword", country="US"
    )

    assert not user.is_italian()
