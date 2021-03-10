from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from ward import fixture

from main import app


@fixture
async def testclient():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client
