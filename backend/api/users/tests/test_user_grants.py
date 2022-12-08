import pytest

from api.grants.types import Grant
from api.users.types import User

pytestmark = pytest.mark.django_db


def test_query_grant(graphql_client, user, conference, grant_factory):
    graphql_client.force_login(user)

    grant = grant_factory(user_id=user.id, conference=conference)

    user = User.resolve_reference(user.id, user.email)
    grant = user.grant(info=None, conference=conference.code)

    assert isinstance(grant, Grant)
    assert grant.id == grant.id
