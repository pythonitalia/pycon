from unittest.mock import patch

from notifications.emails import SafeString, get_email_backend, mark_safe
import pytest


class TestBackend:
    pass


class TestBackendWithEnv:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b


def test_get_email_backend():
    loaded_backend = get_email_backend("notifications.tests.test_emails.TestBackend")
    assert "notifications.tests.test_emails.TestBackend" in str(type(loaded_backend))


def test_loading_same_backend_uses_cache():
    loaded_backend = get_email_backend("notifications.tests.test_emails.TestBackend")
    assert "notifications.tests.test_emails.TestBackend" in str(type(loaded_backend))

    with patch("pythonit_toolkit.emails.utils.importlib.import_module") as mock:
        loaded_backend = get_email_backend(
            "notifications.tests.test_emails.TestBackend"
        )

    assert "notifications.tests.test_emails.TestBackend" in str(type(loaded_backend))
    assert not mock.called

    mock.reset_mock()

    with patch("pythonit_toolkit.emails.utils.importlib.import_module") as mock:
        get_email_backend("notifications.tests.test_emails.TestBackend2")

    assert mock.called


def test_get_email_backend_with_envs():
    loaded_backend = get_email_backend(
        "notifications.tests.test_emails.TestBackendWithEnv", a=1, b=2
    )
    assert loaded_backend.a == 1
    assert loaded_backend.b == 2


def test_mark_safe():
    safe_string = mark_safe("abc")

    assert isinstance(safe_string, SafeString)
    assert str(safe_string) == "abc"


def test_mark_safe_empty_string():
    safe_string = mark_safe("")

    assert isinstance(safe_string, SafeString)
    assert str(safe_string) == ""


def mark_safe_with_none_fails():
    with pytest.raises(ValueError):
        mark_safe(None)
