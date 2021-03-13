from ward import test

from users.tests.factories import user_factory, user_factory_batch
from users.tests.graphql_client import admin_graphql_client
from users.tests.session import db


@test("search users by email")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "user"})
    assert not response.errors
    assert response.data == {
        "search": {"users": [{"id": logged_user.id, "email": logged_user.email}]}
    }


@test("search users fuzzy multiple words")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    another_user = await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(
        query, variables={"query": "user email"}
    )
    assert not response.errors
    assert {"id": logged_user.id, "email": logged_user.email} in response.data[
        "search"
    ]["users"]
    assert {"id": another_user.id, "email": another_user.email} in response.data[
        "search"
    ]["users"]


@test("search users by fullname")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    another_user = await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "Giorg"})
    assert not response.errors
    assert len(response.data["search"]["users"]) == 2
    assert {"id": logged_user.id, "email": logged_user.email} in response.data[
        "search"
    ]["users"]
    assert {"id": another_user.id, "email": another_user.email} in response.data[
        "search"
    ]["users"]


@test("search users empty result")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "Emerlinda"})
    assert not response.errors
    assert len(response.data["search"]["users"]) == 0


@test("search users with empty query returns nothing")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": ""})
    assert not response.errors
    assert len(response.data["search"]["users"]) == 0


@test("cannot search users unlogged")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "Emerlinda"})
    assert response.errors[0]["message"] == "Unauthorized"
    assert not response.data


@test("cannot search users if not staff")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=False,
    )
    admin_graphql_client.force_login(logged_user)

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "Emerlinda"})
    assert response.errors[0]["message"] == "Unauthorized"
    assert not response.data


@test("search users only returns 10 matches")
async def _(
    admin_graphql_client=admin_graphql_client,
    db=db,
    user_factory_batch=user_factory_batch,
    user_factory=user_factory,
):
    logged_user = await user_factory(
        email="user@world.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    await user_factory_batch(
        50,
        email="another-email@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(
        query, variables={"query": "another email"}
    )
    assert not response.errors
    assert len(response.data["search"]["users"]) == 10


@test("search users by fullname")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    another_user = await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "Giorg"})
    assert not response.errors
    assert len(response.data["search"]["users"]) == 2
    assert {"id": logged_user.id, "email": logged_user.email} in response.data[
        "search"
    ]["users"]
    assert {"id": another_user.id, "email": another_user.email} in response.data[
        "search"
    ]["users"]


@test("search users empty result")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "Emerlinda"})
    assert not response.errors
    assert len(response.data["search"]["users"]) == 0


@test("search users with empty query returns nothing")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )
    admin_graphql_client.force_login(logged_user)

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": ""})
    assert not response.errors
    assert len(response.data["search"]["users"]) == 0


@test("cannot search users unlogged")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=True,
    )

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "Emerlinda"})
    assert response.errors[0]["message"] == "Unauthorized"
    assert not response.data


@test("cannot search users if not staff")
async def _(
    admin_graphql_client=admin_graphql_client, db=db, user_factory=user_factory
):
    logged_user = await user_factory(
        email="user@email.it",
        fullname="Giorgina Giogio",
        name="Giorgina",
        is_staff=False,
    )
    admin_graphql_client.force_login(logged_user)

    await user_factory(
        email="another-email@email.it",
        fullname="Giorgina Buonofiglio",
        name="Cattiva",
        is_staff=False,
    )

    query = """query($query: String!) {
        search(query: $query) {
            users {
                id
                email
            }
        }
    }"""

    response = await admin_graphql_client.query(query, variables={"query": "Emerlinda"})
    assert response.errors[0]["message"] == "Unauthorized"
    assert not response.data
