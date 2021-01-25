from typing import Optional

from base.domain.repository import BaseSQLAlchemyRepository
from domain.entities import User
from sqlalchemy.sql.expression import select


class AbstractUsersRepository:
    pass


class UsersRepository(BaseSQLAlchemyRepository):
    async def get(self, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        user = (await self.session.execute(query)).scalar_one_or_none()
        return user

    async def save_user(self, user: User) -> User:
        session = self.session

        async with session.begin():
            session.add(user)

        return user
