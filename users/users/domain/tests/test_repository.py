import datetime
from typing import cast

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from ward import test

from users.domain.entities import User
from users.domain.repository import UsersRepository
from users.tests.factories import user_factory
from users.tests.session import cleanup_db, db, second_session


@test("create user")
async def _(db=db, second_session=second_session, cleanup_db=cleanup_db):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    repository = UsersRepository(db)

    await repository.create_user(
        User(
            email="test@user.it",
            password="hello",
            date_joined=datetime.datetime(2020, 1, 1, 1, tzinfo=datetime.timezone.utc),
            username="username",
            fullname="Nanan Nana",
            gender="male",
            date_birth=datetime.date(2000, 5, 1),
            open_to_newsletter=False,
            open_to_recruiting=True,
            country="IT",
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
    )
    await repository.commit()

    query = select(User).where(User.email == "test@user.it")
    db_user: User = (await second_session.execute(query)).scalar()

    assert db_user
    assert db_user.date_joined == datetime.datetime(
        2020, 1, 1, 1, tzinfo=datetime.timezone.utc
    )
    assert db_user.username == "username"
    assert db_user.fullname == "Nanan Nana"
    assert db_user.gender == "male"
    assert db_user.date_birth == datetime.date(2000, 5, 1)
    assert db_user.open_to_newsletter is False
    assert db_user.open_to_recruiting is True
    assert db_user.country == "IT"
    assert db_user.is_active is True
    assert db_user.is_staff is False
    assert db_user.is_superuser is False


@test("get user by email")
async def _(
    db=db,
    second_session=second_session,
    user_factory=user_factory,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    await user_factory(email="existing@user.it")
    await db.commit()

    repository = UsersRepository(db)
    found_user = await repository.get_by_email("existing@user.it")

    query = select(User).where(User.email == "existing@user.it")
    raw_query_user: User = (await second_session.execute(query)).scalar()

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert found_user.id == raw_query_user.id
    assert found_user.date_joined == raw_query_user.date_joined
    assert found_user.username == raw_query_user.username
    assert found_user.fullname == raw_query_user.fullname
    assert found_user.gender == raw_query_user.gender
    assert found_user.date_birth == raw_query_user.date_birth
    assert found_user.open_to_newsletter is raw_query_user.open_to_newsletter
    assert found_user.open_to_recruiting is raw_query_user.open_to_recruiting
    assert found_user.country == raw_query_user.country
    assert found_user.is_active is raw_query_user.is_active
    assert found_user.is_staff is raw_query_user.is_staff
    assert found_user.is_superuser is raw_query_user.is_superuser


@test("get user by id")
async def _(
    db=db,
    second_session=second_session,
    user_factory=user_factory,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    created_user = await user_factory(id=10, email="existing@user.it")
    await db.commit()

    repository = UsersRepository(db)
    # TODO test if it makes sense
    found_user = await repository.get_by_id(10)

    query = select(User).where(User.id == 10)
    raw_query_user: User = (await second_session.execute(query)).scalar()

    assert found_user.id == created_user.id
    assert found_user.username == created_user.username
    assert found_user.email == created_user.email

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert found_user.id == raw_query_user.id
    assert found_user.date_joined == raw_query_user.date_joined
    assert found_user.username == raw_query_user.username
    assert found_user.fullname == raw_query_user.fullname
    assert found_user.gender == raw_query_user.gender
    assert found_user.date_birth == raw_query_user.date_birth
    assert found_user.open_to_newsletter is raw_query_user.open_to_newsletter
    assert found_user.open_to_recruiting is raw_query_user.open_to_recruiting
    assert found_user.country == raw_query_user.country
    assert found_user.is_active is raw_query_user.is_active
    assert found_user.is_staff is raw_query_user.is_staff
    assert found_user.is_superuser is raw_query_user.is_superuser
