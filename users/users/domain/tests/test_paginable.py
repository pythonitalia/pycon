from ward import raises, test

from users.domain.entities import User
from users.domain.paginable import Paginable
from users.tests.factories import user_factory
from users.tests.session import db


@test("paginate items")
async def _(db=db, user_factory=user_factory):
    user_1 = await user_factory(email="user1@email.it")
    user_2 = await user_factory(email="user2@email.it")
    user_3 = await user_factory(email="user3@email.it")

    paginable = Paginable(db, User)
    page = await paginable.page(0, 1)

    assert page.total_count == 3
    assert page.items == [user_1]

    page = await paginable.page(1, 3)

    assert page.total_count == 3
    assert page.items == [user_2, user_3]


@test("size outside total")
async def _(db=db, user_factory=user_factory):
    user_1 = await user_factory(email="user1@email.it")
    user_2 = await user_factory(email="user2@email.it")
    user_3 = await user_factory(email="user3@email.it")

    paginable = Paginable(db, User)
    page = await paginable.page(0, 1000)

    assert page.total_count == 3
    assert page.items == [user_1, user_2, user_3]


@test("negative after is not allowed")
async def _(db=db, user_factory=user_factory):
    await user_factory(email="user1@email.it")
    await user_factory(email="user2@email.it")
    await user_factory(email="user3@email.it")

    paginable = Paginable(db, User)

    with raises(ValueError) as exc:
        await paginable.page(-10, 1000)

    assert str(exc.raised) == "after cannot be negative"


@test("negative to is not allowed")
async def _(db=db, user_factory=user_factory):
    await user_factory(email="user1@email.it")
    await user_factory(email="user2@email.it")
    await user_factory(email="user3@email.it")

    paginable = Paginable(db, User)

    with raises(ValueError) as exc:
        await paginable.page(0, -100)

    assert str(exc.raised) == "to cannot be negative"
