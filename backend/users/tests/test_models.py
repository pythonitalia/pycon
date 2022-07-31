import pytest

from users.models import User, get_countries


@pytest.mark.django_db
def test_user_get_short_name():
    user = User.objects.create_user("lennon@thebeatles.com", "johnpassword")

    assert "lennon@thebeatles.com" == user.get_short_name()


# region country_utilities


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


def test_get_country():
    country = "IT"
    resp = get_countries(country)
    assert resp["code"] == "IT"
    assert resp["name"] == "Italy"


# endregion
