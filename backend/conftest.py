import pytest
from api.tests.fixtures import *  # noqa
from blog.tests.factories import *  # noqa
from cms.tests.factories import *  # noqa
from conferences.tests.factories import *  # noqa
from django.test.client import Client
from events.tests.factories import *  # noqa
from languages.models import Language
from languages.tests.factories import *  # noqa
from pages.tests.factories import *  # noqa
from schedule.tests.factories import *  # noqa
from sponsors.tests.factories import *  # noqa
from submissions.tests.factories import *  # noqa
from users.models import User
from users.tests.factories import *  # noqa
from voting.tests.factories.vote import *  # noqa


@pytest.fixture()
def user(db):
    user = User._default_manager.create_user("user@example.com", "password")

    return user


@pytest.fixture()
def admin_user(db):
    user = User._default_manager.create_superuser("admin@example.com", "password")

    return user


@pytest.fixture
def language():
    return lambda code: Language.objects.get(code=code)


@pytest.fixture
def http_client():
    return Client()


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
