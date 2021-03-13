from pythonit_toolkit.pastaporto.test import fake_service_to_service_token
from ward import test
from ward.testing import each

from users.settings import SERVICE_JWT_HEADER, SERVICE_TO_SERVICE_SECRET
from users.tests.client import testclient


@test("cannot load internal api without token")
async def _(
    testclient=testclient, method=each("get", "post", "patch", "delete", "options")
):
    response = await getattr(testclient, method)("/internal-api")

    assert response.status_code == 400
    assert response.json() == {"error": "Forbidden"}


@test("cannot load internal api with wrong jwt audience/issuer")
async def _(testclient=testclient):
    fake_token = fake_service_to_service_token(
        SERVICE_TO_SERVICE_SECRET, issuer="another-service", audience="another"
    )

    response = await testclient.post(
        "/internal-api", headers={SERVICE_JWT_HEADER: fake_token}
    )

    assert response.status_code == 400
    assert response.json() == {"error": "Forbidden"}
