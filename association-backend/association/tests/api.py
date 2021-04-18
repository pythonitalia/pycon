from asgi_lifespan import LifespanManager
from association.settings import PASTAPORTO_SECRET
from httpx import AsyncClient
from main import app
from pythonit_toolkit.api.graphql_test_client import GraphQLClient
from ward import fixture


@fixture
async def testclient():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client


@fixture()
async def graphql_client(testclient=testclient):
    async with testclient:
        yield GraphQLClient(testclient, pastaporto_secret=PASTAPORTO_SECRET)


@fixture()
async def admin_graphql_client(testclient=testclient):
    async with testclient:
        yield GraphQLClient(
            testclient, admin_endpoint=True, pastaporto_secret=PASTAPORTO_SECRET
        )
