import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory
from users.domain.entities import User
from users.starlette_password.hashers import make_password
from ward import fixture

from .session import test_session


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = test_session

    username = "user"
    email = "user@pycon.it"
    fullname = "First Last"
    name = "First"
    gender = "male"
    is_active = True
    is_staff = False
    is_superuser = False
    date_birth = None
    open_to_recruiting = False
    open_to_newsletter = False
    country = "US"
    date_joined = datetime.datetime.now()

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if not create:
            return

        password = extracted or "user"
        obj.hashed_password = make_password(password)
        return None


@fixture
async def user_factory():
    async def func(**kwargs):
        obj = UserFactory.create(**kwargs)
        await UserFactory._meta.sqlalchemy_session.flush()
        return obj

    return func
