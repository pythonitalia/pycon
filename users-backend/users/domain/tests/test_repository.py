import datetime
from typing import cast

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from ward import test

from users.domain.entities import User
from users.domain.repository import UsersRepository
from users.tests.factories import user_factory
from users.tests.session import db, second_session


@test("create user")
async def _(db=db, second_session=second_session):
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


@test("get all users")
async def _(db=db, second_session=second_session, user_factory=user_factory):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    user = await user_factory(email="user1@user.it", id=1)
    user_2 = await user_factory(email="user2@user.it", id=2)
    user_3 = await user_factory(email="user3@user.it", id=3)

    repository = UsersRepository(db)
    paginable = await repository.get_users()

    page = await paginable.page(0, 1)

    assert page.total_count == 3
    assert page.items[0].id == user.id

    page = await paginable.page(1, 3)
    assert page.total_count == 3
    assert [i.id for i in page.items] == [user_2.id, user_3.id]


@test("get user by email")
async def _(
    db=db,
    second_session=second_session,
    user_factory=user_factory,
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


@test("search users")
async def _(db=db, user_factory=user_factory):
    user_1 = await user_factory(email="marco@email.it", fullname="Marco Ciao", name="")
    await user_factory(email="nina@email.it", fullname="Nina Nana", name="")
    await user_factory(email="patrick@email.it", fullname="Patrick Ciao", name="")

    repository = UsersRepository(db)
    found_users = await repository.search("Marco")

    assert len(found_users) == 1
    assert found_users[0].id == user_1.id


@test("search users is case-insensitive")
async def _(db=db, user_factory=user_factory):
    user_1 = await user_factory(email="marco@email.it", fullname="Marco Ciao", name="")
    await user_factory(email="nina@email.it", fullname="Nina Nana", name="")
    user_3 = await user_factory(
        email="patrick@email.it", fullname="Patrick Ciao", name=""
    )

    repository = UsersRepository(db)
    found_users = await repository.search("ciao")

    assert len(found_users) == 2
    ids = [u.id for u in found_users]

    assert user_1.id in ids
    assert user_3.id in ids


@test("search users returns empty if there are no results")
async def _(db=db, user_factory=user_factory):
    await user_factory(email="marco@email.it", fullname="Marco Ciao", name="")
    await user_factory(email="nina@email.it", fullname="Nina Nana", name="")
    await user_factory(email="patrick@email.it", fullname="Patrick Ciao", name="")

    repository = UsersRepository(db)
    found_users = await repository.search("nono")

    assert len(found_users) == 0


@test("search users by email")
async def _(db=db, user_factory=user_factory):
    await user_factory(email="marco@email.it", fullname="Marco Ciao", name="")
    await user_factory(email="nina@email.it", fullname="Nina Nana", name="")
    user = await user_factory(
        email="ohhello@email.it", fullname="Not In my name", name=""
    )

    repository = UsersRepository(db)
    found_users = await repository.search("ohhello")

    assert len(found_users) == 1
    assert found_users[0].id == user.id


@test("search users by email, fullname and name")
async def _(db=db, user_factory=user_factory):
    user_1 = await user_factory(email="marco@email.it", fullname="Hello Ciao", name="")
    user_2 = await user_factory(
        email="nina@email.it", fullname="Nina Nana", name="Nope Hello!"
    )
    user_3 = await user_factory(
        email="ohhello@email.it", fullname="Not In my name", name=""
    )
    await user_factory(email="notincluded@email.it", fullname="Ciao mondo!", name="")

    repository = UsersRepository(db)
    found_users = await repository.search("hello")

    assert len(found_users) == 3
    ids = [u.id for u in found_users]

    assert user_1.id in ids
    assert user_2.id in ids
    assert user_3.id in ids


@test("search users by multiple words")
async def _(db=db, user_factory=user_factory):
    user_1 = await user_factory(email="marco@email.it", fullname="Hello Ciao", name="")
    user_2 = await user_factory(
        email="nina@email.it", fullname="Nina Nana", name="Nope Hello!"
    )
    await user_factory(email="ohhello@email.it", fullname="Not In my name", name="")

    repository = UsersRepository(db)
    found_users = await repository.search("Nina Ciao")

    assert len(found_users) == 2
    ids = [u.id for u in found_users]

    assert user_1.id in ids
    assert user_2.id in ids


@test("cannot search users by empty query")
async def _(db=db, user_factory=user_factory):
    await user_factory(email="marco@email.it", fullname="Hello Ciao", name="")
    await user_factory(email="nina@email.it", fullname="Nina Nana", name="Nope Hello!")
    await user_factory(email="ohhello@email.it", fullname="Not In my name", name="")
    await user_factory(email="notincluded@email.it", fullname="Ciao mondo!", name="")

    repository = UsersRepository(db)
    found_users = await repository.search("")

    assert len(found_users) == 0


@test("get multiple users by id")
async def _(db=db, user_factory=user_factory):
    u1 = await user_factory(email="marco@email.it", fullname="Hello Ciao", name="")
    u2 = await user_factory(
        email="nina@email.it", fullname="Nina Nana", name="Nope Hello!"
    )
    u3 = await user_factory(
        email="ohhello@email.it", fullname="Not In my name", name=""
    )
    u4 = await user_factory(
        email="notincluded@email.it", fullname="Ciao mondo!", name=""
    )

    repository = UsersRepository(db)
    users = await repository.get_batch_by_ids([u1.id, u2.id, u3.id])

    assert len(users) == 3
    found_ids = [u.id for u in users]

    assert u1.id in found_ids
    assert u2.id in found_ids
    assert u3.id in found_ids
    assert u4.id not in found_ids
