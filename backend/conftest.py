from wagtail.models import Locale
from django.core.files.images import ImageFile
import os
from io import BytesIO
import PIL.Image
import base64
from rest_framework.test import APIClient

import pytest
from django.test.client import Client

from api.tests.factories import *  # noqa
from api.tests.fixtures import *  # noqa
from blog.tests.factories import *  # noqa
from checklist.tests.factories import *  # noqa
from cms.tests.factories import *  # noqa
from conferences.tests.factories import *  # noqa
from events.tests.factories import *  # noqa
from grants.tests.factories import *  # noqa
from hotels.tests.factories import *  # noqa
from job_board.tests.factories import *  # noqa
from languages.models import Language
from languages.tests.factories import *  # noqa
from newsletters.tests.factories import *  # noqa
from pages.tests.factories import *  # noqa
from participants.tests.factories import *  # noqa
from pretix.tests.fixtures import *  # noqa
from reviews.tests.factories import *  # noqa
from schedule.tests.factories import *  # noqa
from sponsors.tests.factories import *  # noqa
from submissions.tests.factories import *  # noqa
from users.tests.factories import *  # noqa
from voting.tests.factories import *  # noqa
from voting.tests.fixtures import *  # noqa
from users.tests.factories import UserFactory
from api.cms.tests.factories import *  # noqa


@pytest.fixture()
def user(db):
    return UserFactory(email="simulated@user.it", is_staff=False)


@pytest.fixture()
def admin_user(db):
    return UserFactory(email="admin@user.it", is_staff=True)


@pytest.fixture
def language():
    return lambda code: Language.objects.get(code=code)


@pytest.fixture
def http_client():
    return Client()


@pytest.fixture
def rest_api_client():
    api_client = APIClient()
    api_client.basic_auth = lambda username, password: api_client.credentials(
        HTTP_AUTHORIZATION="Basic "
        + base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
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


@pytest.fixture(autouse=True)
def change_azure_account_to_test_name(settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "pytest-fakestorageaccount"


class TestEmailBackend:
    ALL_EMAIL_BACKEND_CALLS = []

    def __init__(self, *args, **kwargs) -> None:
        pass

    def send_email(self, **kwargs):
        TestEmailBackend.ALL_EMAIL_BACKEND_CALLS.append(kwargs)


@pytest.fixture
def sent_emails():
    TestEmailBackend.ALL_EMAIL_BACKEND_CALLS = []
    yield TestEmailBackend.ALL_EMAIL_BACKEND_CALLS


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
