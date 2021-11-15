from unittest.mock import MagicMock

from pythonit_toolkit.api.permissions import IsService
from pythonit_toolkit.headers import SERVICE_JWT_HEADER
from pythonit_toolkit.pastaporto.tokens import generate_service_to_service_token
from ward import fixture, raises, test


@fixture
def fake_info():
    def _fake_info(token):
        headers = {SERVICE_JWT_HEADER: token}
        mock_info = MagicMock()
        mock_info.context.request.headers.get = headers.get
        return mock_info

    return _fake_info


@test("Allowed callers pass the permission")
async def _(fake_info=fake_info):
    test_token = generate_service_to_service_token("test", "gateway", "users-backend")
    mock_info = fake_info(test_token)

    PermissionClass = IsService(["gateway"], "test", "users-backend")

    assert PermissionClass().has_permission(None, mock_info) is True


@test("Not allowed callers fail the permission")
async def _(fake_info=fake_info):
    test_token = generate_service_to_service_token(
        "test", "pycon-backend", "users-backend"
    )
    mock_info = fake_info(test_token)

    PermissionClass = IsService(["gateway"], "test", "users-backend")

    assert PermissionClass().has_permission(None, mock_info) is False


@test("Multiple allowed callers pass the permission")
async def _(fake_info=fake_info):
    test_token = generate_service_to_service_token(
        "test", "association-backend", "users-backend"
    )
    mock_info = fake_info(test_token)

    PermissionClass = IsService(
        ["gateway", "association-backend"], "test", "users-backend"
    )

    assert PermissionClass().has_permission(None, mock_info) is True


@test("Wrong secret fail permission")
async def _(fake_info=fake_info):
    test_token = generate_service_to_service_token(
        "wrong-secret", "pycon-backend", "users-backend"
    )
    mock_info = fake_info(test_token)

    PermissionClass = IsService(["gateway"], "test", "users-backend")

    assert PermissionClass().has_permission(None, mock_info) is False


@test("Token for another service fails permission")
async def _(fake_info=fake_info):
    test_token = generate_service_to_service_token("test", "pycon-backend", "gateway")
    mock_info = fake_info(test_token)

    PermissionClass = IsService(["pycon-backend"], "test", "users-backend")

    assert PermissionClass().has_permission(None, mock_info) is False


@test("Cannot create a permission not allowing any service")
async def _():
    with raises(ValueError) as exc:
        IsService([], "test", "users-backend")

    assert str(exc.raised) == "No callers allowed specified"


@test("Cannot create a permission without any secret")
async def _():
    with raises(ValueError) as exc:
        IsService(["service"], "", "users-backend")

    assert str(exc.raised) == "JWT secret cannot be empty"


@test("Cannot create a permission without the current service name")
async def _():
    with raises(ValueError) as exc:
        IsService(["service"], "secret", "")

    assert str(exc.raised) == "Current service name cannot be empty"
