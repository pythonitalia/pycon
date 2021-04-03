from unittest.mock import patch

from pythonit_toolkit.emails.utils import get_email_backend
from ward import test


class TestBackend:
    pass


class TestBackendWithEnv:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b


@test("get email backend")
async def _():
    loaded_backend = get_email_backend("tests.emails.test_utils.TestBackend")
    assert "tests.emails.test_utils.TestBackend" in str(type(loaded_backend))


@test("loading the same backend path uses the cache")
async def _():
    loaded_backend = get_email_backend("tests.emails.test_utils.TestBackend")
    assert "tests.emails.test_utils.TestBackend" in str(type(loaded_backend))

    with patch("pythonit_toolkit.emails.utils.importlib.import_module") as mock:
        loaded_backend = get_email_backend("tests.emails.test_utils.TestBackend")

    assert "tests.emails.test_utils.TestBackend" in str(type(loaded_backend))
    assert not mock.called

    mock.reset_mock()

    with patch("pythonit_toolkit.emails.utils.importlib.import_module") as mock:
        get_email_backend("tests.emails.test_utils.TestBackend2")

    assert mock.called


@test("get email backend passing environment variables")
async def _():
    loaded_backend = get_email_backend(
        "tests.emails.test_utils.TestBackendWithEnv", a=1, b=2
    )
    assert loaded_backend.a == 1
    assert loaded_backend.b == 2
