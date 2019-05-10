import pytest

from users.models import User
from languages.models import Language

from .api.fixtures import *  # noqa
from .conferences.factories import *  # noqa
from .submissions.factories import *  # noqa
from .schedule.factories import *  # noqa
from .languages.factories import *  # noqa
from .users.factories import *  # noqa


@pytest.fixture()
def user(db):
    user = User._default_manager.create_user("user@example.com", "password")

    return user


@pytest.fixture()
def admin_user(db):
    user = User._default_manager.create_superuser(
        "admin@example.com", "password"
    )

    return user

@pytest.fixture
def language():
    return lambda code: Language.objects.get(code=code)
