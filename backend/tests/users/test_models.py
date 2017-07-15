from django.contrib.auth import authenticate, get_user_model

import pytest
from users.models import User


def test_that_get_user_model_returns_correct_model():
    assert get_user_model() == User


@pytest.mark.django_db
def test_create_user_with_email_and_password():
    user = User.objects.create_user('lennon@thebeatles.com', 'johnpassword')

    assert user.email == 'lennon@thebeatles.com'


@pytest.mark.django_db
def test_create_user_and_authenticate():
    user = User.objects.create_user('lennon@thebeatles.com', 'johnpassword')

    authenticated_user = authenticate(
        username='lennon@thebeatles.com', password='johnpassword'
    )

    assert user == authenticated_user
