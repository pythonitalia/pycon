from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pythonit_toolkit.api.graphql_test_client import GraphQLClient
from ward import fixture

from main import app
from src.association.settings import PASTAPORTO_SECRET


@fixture
async def testclient():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client


@fixture()
async def graphql_client(testclient=testclient):
    yield GraphQLClient(testclient, pastaporto_secret=PASTAPORTO_SECRET)
