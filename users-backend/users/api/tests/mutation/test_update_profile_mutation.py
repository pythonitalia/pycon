from sqlalchemy.sql.expression import select
from ward import test

from users.domain.entities import User
from users.tests.api import graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("update profile")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    user = await user_factory(email="test@email.it", password="hello", jwt_auth_id=1)

    graphql_client.force_login(user)

    query = """mutation($input: UpdateProfileInput!) {
        updateProfile(input: $input) {
            __typename

            ... on User {
                id
                name
                fullName
                gender
                openToRecruiting
                openToNewsletter
                country
                dateBirth
            }
        }
    }"""

    response = await graphql_client.query(
        query,
        variables={
            "input": {
                "name": "Name",
                "fullName": "Fullname",
                "gender": "male",
                "openToRecruiting": False,
                "openToNewsletter": True,
                "country": "IT",
                "dateBirth": None,
            }
        },
    )

    assert not response.errors
    query = select(User).where(User.email == "test@email.it")
    raw_query_user: User = (await db.execute(query)).scalar()

    assert raw_query_user.name == "Name"
    assert raw_query_user.fullname == "Fullname"
    assert raw_query_user.gender == "male"
    assert raw_query_user.open_to_recruiting is False
    assert raw_query_user.open_to_newsletter is True
    assert raw_query_user.country == "IT"
    assert raw_query_user.date_birth is None
