from ward import test

from users.tests.factories import user_factory
from users.tests.graphql_client import admin_graphql_client
from users.tests.session import db


@test("unlogged cannot fetch me")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    user = await user_factory(email="user@email.it", is_staff=False)
    admin_graphql_client.force_login(user)

    query = """query {
        me {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query)
    assert response.errors[0]["message"] == "Unauthorized"


@test("fetch me")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(email="user@email.it", is_staff=True)
    admin_graphql_client.force_login(logged_user)

    query = """query {
        me {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query)
    assert not response.errors
    assert response.data["me"] == {"id": logged_user.id, "email": logged_user.email}


@test("only staff accounts can fetch me")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(email="user@email.it", is_staff=False)
    admin_graphql_client.force_login(logged_user)

    query = """query {
        me {
            id
            email
        }
    }"""

    response = await admin_graphql_client.query(query)
    assert response.errors[0]["message"] == "Unauthorized"
