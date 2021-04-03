from ward import test

from users.tests.factories import user_factory
from users.tests.graphql_client import admin_graphql_client
from users.tests.session import db


@test("unlogged cannot fetch user")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    user = await user_factory(email="user@email.it", is_staff=False)

    query = """query($id: ID!) {
        user(id: $id) {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"id": user.id})
    assert response.errors[0]["message"] == "Unauthorized"


@test("only staff can fetch user details")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(email="user@email.it", is_staff=False)
    admin_graphql_client.force_login(logged_user)

    user = await user_factory(email="user2@email.it", is_staff=False)

    query = """query($id: ID!) {
        user(id: $id) {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"id": user.id})
    assert response.errors[0]["message"] == "Unauthorized"


@test("fetch user")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    admin = await user_factory(email="staff@email.it", password="test", is_staff=True)
    admin_graphql_client.force_login(admin)

    user_1 = await user_factory(email="user1@email.it", password="test")

    query = """query($id: ID!) {
        user(id: $id) {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"id": user_1.id})

    assert not response.errors
    assert {"id": user_1.id, "email": user_1.email} == response.data["user"]
