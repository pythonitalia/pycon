from ward import test
from ward.testing import each

from users.tests.client import testclient


@test("cannot load internal api without token")
async def _(
    testclient=testclient, method=each("get", "post", "patch", "delete", "options")
):
    response = await getattr(testclient, method)("/internal-api")

    assert response.status_code == 400
    assert response.json() == {"error": "Forbidden"}
