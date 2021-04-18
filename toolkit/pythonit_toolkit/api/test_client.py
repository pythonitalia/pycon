from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from main import app
from ward import fixture


@fixture
async def testclient():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client
