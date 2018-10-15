from api.settings import LIMIT_MAX_VALUE, LIMIT_MIN_VALUE, LIMIT_DEFAULT_VALUE


def _query_all_users(client, offset, limit=LIMIT_DEFAULT_VALUE):
    return client.query(
        """
        query($offset: Int!, $limit: Int!) {
            users(offset: $offset, limit: $limit) {
                totalCount
                objects {
                    id
                    email
                }
            }
        }
        """,
        variables={
            "offset": offset,
            "limit": limit
        }
    )


def _query_user(client, user_id):
    return client.query(
        """
        query($user: Int!) {
            user(id: $user) {
                id
                email
            }
        }
        """,
        variables={
            "user": user_id,
        }
    )


def test_fails_when_user_is_not_authenticated(graphql_client):
    resp = graphql_client.query(
        """
        {
            me {
                email
            }
        }
        """
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


def test_works_when_user_is_logged_in(user, graphql_client):
    graphql_client.force_login(user)

    resp = graphql_client.query(
        """
        {
            me {
                email
            }
        }
        """
    )

    assert "errors" not in resp
    assert resp["data"]["me"]["email"] == user.email


def test_query_all_users_works_only_when_logged_in(graphql_client):
    resp = _query_all_users(graphql_client, 0)

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


def test_query_all_users_works_only_for_superstaff_users(user, graphql_client):
    graphql_client.force_login(user)

    resp = _query_all_users(graphql_client, 0)

    assert "errors" in resp
    assert resp["errors"][0]["message"] == "You don't have the permissions"
    assert resp["data"] is None


def test_query_all_users(admin_user, user_factory, graphql_client):
    graphql_client.force_login(admin_user)

    users = [user_factory() for i in range(5)]
    users.append(admin_user)

    resp = _query_all_users(graphql_client, 0)

    assert "errors" not in resp
    assert resp["data"]["users"]["totalCount"] == len(users)
    assert len(resp["data"]["users"]["objects"]) == len(users)

    for test_user in users:
        assert {
            'id': str(test_user.id),
            'email': test_user.email
        } in resp["data"]["users"]["objects"]


def test_get_paginated_users(admin_user, user_factory, graphql_client):
    graphql_client.force_login(admin_user)

    users = [user_factory() for i in range(5)]
    users.append(admin_user)
    users = sorted(users, key=lambda u: u.date_joined, reverse=True)

    resp = _query_all_users(graphql_client, 0, 2)

    assert "errors" not in resp
    assert resp["data"]["users"]["totalCount"] == len(users)
    assert len(resp["data"]["users"]["objects"]) == 2

    assert {
        'id': str(users[0].id),
        'email': users[0].email
    } == resp["data"]["users"]["objects"][0]

    assert {
        'id': str(users[1].id),
        'email': users[1].email
    } == resp["data"]["users"]["objects"][1]

    # request another page

    resp = _query_all_users(graphql_client, 2, 2)

    assert "errors" not in resp
    assert resp["data"]["users"]["totalCount"] == len(users)
    assert len(resp["data"]["users"]["objects"]) == 2

    assert {
        'id': str(users[2].id),
        'email': users[2].email
    } == resp["data"]["users"]["objects"][0]

    assert {
        'id': str(users[3].id),
        'email': users[3].email
    } == resp["data"]["users"]["objects"][1]


def test_request_users_with_limit_outside_allowed_value(admin_user, user_factory, graphql_client):
    graphql_client.force_login(admin_user)

    users = [user_factory() for i in range(100)]
    users.append(admin_user)

    resp = _query_all_users(graphql_client, 0, 100)

    assert "errors" not in resp
    assert resp["data"]["users"]["totalCount"] == len(users)
    assert len(resp["data"]["users"]["objects"]) == LIMIT_MAX_VALUE


def test_request_users_with_limit_below_min(admin_user, user_factory, graphql_client):
    graphql_client.force_login(admin_user)

    users = [user_factory() for i in range(100)]
    users.append(admin_user)

    resp = _query_all_users(graphql_client, 0, -5)

    assert "errors" not in resp
    assert resp["data"]["users"]["totalCount"] == len(users)
    assert len(resp["data"]["users"]["objects"]) == LIMIT_MIN_VALUE


def test_get_user_info(admin_user, user_factory, graphql_client):
    graphql_client.force_login(admin_user)
    user = user_factory()

    resp = _query_user(graphql_client, user.id)

    assert "errors" not in resp
    assert {
        'id': str(user.id),
        'email': user.email
    } == resp["data"]["user"]


def test_get_user_requires_admin_permissions(user, user_factory, graphql_client):
    graphql_client.force_login(user)
    another_user = user_factory()

    resp = _query_user(graphql_client, another_user.id)

    assert "errors" in resp
    assert resp["errors"][0]["message"] == "You don't have the permissions"


def test_get_user_requires_logged_user(user, user_factory, graphql_client):
    another_user = user_factory()

    resp = _query_user(graphql_client, another_user.id)

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


def test_get_user_info_with_invalid_id(admin_user, user_factory, graphql_client):
    graphql_client.force_login(admin_user)

    resp = _query_user(graphql_client, 999)

    assert "errors" in resp
    assert resp["errors"][0]["message"] == "User with ID 999 does not exist"
