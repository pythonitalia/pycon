import pytest
from django.test.client import Client
from pythonit_toolkit.api.graphql_test_client import SimulatedUser

from api.tests.factories import *  # noqa
from api.tests.fixtures import *  # noqa
from blog.tests.factories import *  # noqa
from cms.tests.factories import *  # noqa
from conferences.tests.factories import *  # noqa
from events.tests.factories import *  # noqa
from hotels.tests.factories import *  # noqa
from languages.models import Language
from languages.tests.factories import *  # noqa
from newsletters.tests.factories import *  # noqa
from pages.tests.factories import *  # noqa
from schedule.tests.factories import *  # noqa
from sponsors.tests.factories import *  # noqa
from submissions.tests.factories import *  # noqa
from voting.tests.factories import *  # noqa
from voting.tests.fixtures import *  # noqa


@pytest.fixture()
def user(db):
    return SimulatedUser(id=1, email="simulated@user.it", is_staff=False)


@pytest.fixture()
def user_factory(db):
    def func(is_staff=False):
        return SimulatedUser(id=1, email="simulated@user.it", is_staff=is_staff)

    return func


@pytest.fixture()
def admin_user(db):
    return SimulatedUser(id=1, email="admin@user.it", is_staff=True)


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
