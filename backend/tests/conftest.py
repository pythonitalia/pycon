import pytest
from django.test.client import Client
from languages.models import Language
from users.models import User

from .api.fixtures import *  # noqa
from .conferences.factories import *  # noqa
from .languages.factories import *  # noqa
from .orders.factories import *  # noqa
from .schedule.factories import *  # noqa
from .submissions.factories import *  # noqa
from .tickets.factories import *  # noqa
from .users.factories import *  # noqa
from .voting.factories.vote import *  # noqa
from .blog.factories import *  # noqa


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
