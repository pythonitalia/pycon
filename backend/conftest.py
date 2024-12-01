from wagtail.models import Locale
from django.core.files.images import ImageFile
import os
from io import BytesIO
import PIL.Image
import base64
from rest_framework.test import APIClient

import pytest
from django.test.client import Client

from languages.models import Language
from users.tests.factories import UserFactory

from api.tests.fixtures import *  # noqa
from pretix.tests.fixtures import *  # noqa


@pytest.fixture()
def user(db):
    return UserFactory(email="simulated@user.it", is_staff=False, full_name="Jane Doe")


@pytest.fixture()
def admin_user(db):
    return UserFactory(email="admin@user.it", is_staff=True)


@pytest.fixture()
def admin_superuser(db):
    return UserFactory(email="admin@user.it", is_staff=True, is_superuser=True)


@pytest.fixture
def language():
    return lambda code: Language.objects.get(code=code)


@pytest.fixture
def http_client():
    return Client()


@pytest.fixture
def rest_api_client():
    api_client = APIClient()
    api_client.default_format = "json"
    api_client.basic_auth = lambda username, password: api_client.credentials(
        HTTP_AUTHORIZATION="Basic "
        + base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
    )
    api_client.token_auth = lambda token: api_client.credentials(
        HTTP_AUTHORIZATION=f"Token {token}"
    )
    return api_client


def pytest_addoption(parser):
    parser.addoption(
        "--integration", action="store_true", help="run integration tests only"
    )


def pytest_runtest_setup(item):
    run_integration = item.config.getoption("--integration")

    if run_integration and "integration" not in item.keywords:
        pytest.skip("skipping test not marked as integration")
    elif "integration" in item.keywords and not run_integration:
        pytest.skip("pass --integration option to pytest to run this test")


@pytest.fixture
def image_file():
    def wrapper(filename: str = "test.jpg"):
        file = BytesIO()
        image = PIL.Image.new("RGB", (640, 480), "white")
        image.save(file, "JPEG")

        yield ImageFile(file, name=filename)

        os.remove(filename)

    return wrapper


@pytest.fixture
def locale():
    return lambda code: Locale.objects.get_or_create(language_code=code)[0]


@pytest.fixture
def mock_has_ticket(requests_mock, settings):
    def wrapper(conference):
        requests_mock.post(
            f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
            json={"user_has_admission_ticket": True},
        )

    return wrapper
