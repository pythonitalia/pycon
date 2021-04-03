from users.domain.entities import User
from users.domain.paginable import Paginable
from users.tests.factories import user_factory
from users.tests.session import db
from ward import raises, test


@test("paginate items")
async def _(db=db, user_factory=user_factory):
    user_1 = await user_factory(email="user1@email.it")
    user_2 = await user_factory(email="user2@email.it")
    user_3 = await user_factory(email="user3@email.it")

    paginable = Paginable(db, User)
    page = await paginable.page(0, 1)

    assert page.total_count == 3
    assert page.items[0].id == user_1.id

    page = await paginable.page(1, 3)

    assert page.total_count == 3
    assert page.items[0].id == user_2.id
    assert page.items[1].id == user_3.id


@test("size outside total")
async def _(db=db, user_factory=user_factory):
    user_1 = await user_factory(email="user1@email.it")
    user_2 = await user_factory(email="user2@email.it")
    user_3 = await user_factory(email="user3@email.it")

    paginable = Paginable(db, User)
    page = await paginable.page(0, 1000)

    assert page.total_count == 3
    assert [i.id for i in page.items] == [user_1.id, user_2.id, user_3.id]


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
