from typing import Optional

from users.domain.entities import User
from users.domain.repository import AbstractUsersRepository


class FakeUsersRepository(AbstractUsersRepository):
    def __init__(self, users: list[User]) -> None:
        super().__init__()

        self.USERS_BY_EMAIL = {user.email: user for user in users}
        self.USERS_BY_ID = {user.id: user for user in users}

    async def get_by_email(self, email: str) -> Optional[User]:
        return self.USERS_BY_EMAIL.get(email, None)

    async def get_by_id(self, id: int) -> Optional[User]:
        return self.USERS_BY_ID.get(id, None)
