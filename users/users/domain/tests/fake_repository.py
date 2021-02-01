import dataclasses
from typing import Optional

from users.domain.entities import User
from users.domain.repository import AbstractUsersRepository


class DummyTransaction:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        pass


class FakeUsersRepository(AbstractUsersRepository):
    committed: bool = False
    rolledback: bool = False
    _id_counter: int = 1

    def __init__(self, users: list[User]) -> None:
        super().__init__()

        self.USERS_BY_EMAIL = {user.email: user for user in users}
        self.USERS_BY_ID = {user.id: user for user in users}

    async def get_by_email(self, email: str) -> Optional[User]:
        return self.USERS_BY_EMAIL.get(email, None)

    async def get_by_id(self, id: int) -> Optional[User]:
        return self.USERS_BY_ID.get(id, None)

    async def create_user(self, user: User) -> User:
        self._id_counter = self._id_counter + 1

        new_user = dataclasses.replace(
            user, id=self._id_counter, password=user.password
        )
        self.USERS_BY_EMAIL[new_user.email] = new_user
        self.USERS_BY_ID[new_user.id] = new_user
        return new_user

    def transaction(self):
        return DummyTransaction()

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolledback = True
