from ward import test

from users.api.tests.graphql_client import admin_graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("unlogged cannot fetch users")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    await user_factory(email="user@email.it", is_staff=False)

    query = """{
        users {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query)
    assert response.errors[0]["message"] == "Unauthorized"


@test("only staff can fetch users")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(email="user@email.it", is_staff=False)
    admin_graphql_client.force_login(logged_user)

    query = """{
        users {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query)
    assert response.errors[0]["message"] == "Unauthorized"


@test("fetch all users")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    admin = await user_factory(email="staff@email.it", password="test", is_staff=True)
    admin_graphql_client.force_login(admin)

    user1 = await user_factory(email="user1@email.it", password="test")
    user2 = await user_factory(email="user2@email.it", password="test")
    user3 = await user_factory(email="user3@email.it", password="test")

    query = """{
        users {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query)

    assert not response.errors
    assert {"id": user1.id, "email": user1.email} in response.data["users"]
    assert {"id": user2.id, "email": user2.email} in response.data["users"]
    assert {"id": user3.id, "email": user3.email} in response.data["users"]
