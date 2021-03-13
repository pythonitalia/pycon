from ward import test

from users.tests.factories import user_factory
from users.tests.graphql_client import internalapi_graphql_client
from users.tests.session import db


@test("get user by id")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login()

    user = await user_factory(email="testuser@user.it", is_staff=False)

    query = """query($id: ID!) {
        user(id: $id) {
            id
            email
            isStaff
        }
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": user.id})
    assert not response.errors
    assert {"id": user.id, "email": user.email, "isStaff": False} == response.data[
        "user"
    ]


@test("get user by not existent id")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login()

    await user_factory(email="testuser@user.it", is_staff=False)

    query = """query($id: ID!) {
        user(id: $id) {
            id
            email
            isStaff
        }
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": 100})
    assert not response.errors
    assert response.data["user"] is None
