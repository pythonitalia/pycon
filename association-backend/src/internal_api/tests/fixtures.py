from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pythonit_toolkit.api.graphql_test_client import GraphQLClient
from ward import Scope, fixture

from main import app
from src.association.settings import PASTAPORTO_SECRET, SERVICE_TO_SERVICE_SECRET


@fixture(scope=Scope.Global)
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client


@fixture
async def testclient(client=client):
    async with LifespanManager(app):
        yield client


@fixture
async def internalapi_graphql_client(testclient=testclient):
    yield GraphQLClient(
        testclient,
        internal_api_endpoint=True,
        pastaporto_secret=PASTAPORTO_SECRET,
        service_to_service_secret=SERVICE_TO_SERVICE_SECRET,
    )
